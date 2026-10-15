<?php
/**
 * EHI Heating & Cooling quote form handler.
 * Validates the request, emails it to the business inbox, and keeps a backup copy
 * outside the web root so no lead is lost if email delivery fails.
 */
declare(strict_types=1);

const LEAD_TO     = 'efficienthomecomfort@gmail.com';
const LEAD_CC     = 'seo@weblab4u.com';
const SITE_NAME   = 'EHI Heating & Cooling website';
const MAX_PER_HOUR = 12;                      // real submissions per IP per hour (offices can share one IP)

header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

function out(int $code, array $body): void {
    http_response_code($code);
    echo json_encode($body);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    out(405, ['ok' => false, 'error' => 'Use POST.']);
}

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

/**
 * Hand the message to sendmail directly with a hard time limit, so a slow or stuck
 * mail server can never leave PHP processes hanging (shared hosting caps processes).
 * Falls back to mail() where proc_open is disabled.
 */
function send_mail(string $to, string $subject, string $body, array $headers, string $from): bool {
    @set_time_limit(30);
    $disabled = array_map('trim', explode(',', (string)ini_get('disable_functions')));
    $sendmail = trim((string)ini_get('sendmail_path')) ?: '/usr/sbin/sendmail -t -i';
    if (function_exists('proc_open') && !in_array('proc_open', $disabled, true)) {
        $proc = @proc_open($sendmail . ' -f ' . escapeshellarg($from), [0 => ['pipe', 'r'], 1 => ['pipe', 'w'], 2 => ['pipe', 'w']], $pipes);
        if (is_resource($proc)) {
            fwrite($pipes[0], "To: $to\r\nSubject: $subject\r\n" . implode("\r\n", $headers) . "\r\n\r\n" . str_replace("\n", "\r\n", $body) . "\r\n");
            fclose($pipes[0]);
            $deadline = microtime(true) + 10;
            do { $st = proc_get_status($proc); if (!$st['running']) break; usleep(100000); } while (microtime(true) < $deadline);
            if ($st['running']) proc_terminate($proc, 9);
            @fclose($pipes[1]); @fclose($pipes[2]); proc_close($proc);
            return !$st['running'] && $st['exitcode'] === 0;
        }
    }
    return @mail($to, $subject, $body, implode("\r\n", $headers), '-f' . $from);
}

/**
 * Private mail settings live OUTSIDE the web root (and outside the public git repo):
 *   <domain folder>/ehi-mail-config.php  ->  <?php return ['smtp_user' => '...', 'smtp_pass' => '...'];
 * When present, leads are sent through Google's SMTP server with that account, which passes
 * Gmail's sender checks. Without it, the handler falls back to the server's sendmail.
 */
function mail_config(): ?array {
    $file = dirname(__DIR__, 2) . '/ehi-mail-config.php';
    if (!is_file($file)) return null;
    $c = include $file;
    return (is_array($c) && !empty($c['smtp_user']) && !empty($c['smtp_pass'])) ? $c : null;
}

function smtp_send(array $cfg, array $rcpts, string $data, string &$err): bool {
    $host = $cfg['smtp_host'] ?? 'ssl://smtp.gmail.com';
    $port = (int)($cfg['smtp_port'] ?? 465);
    $fp = @stream_socket_client("$host:$port", $no, $str, 10, STREAM_CLIENT_CONNECT);
    if (!$fp) { $err = "connect: $str"; return false; }
    stream_set_timeout($fp, 10);
    $read = function () use ($fp): string { $out = ''; while (($l = fgets($fp, 515)) !== false) { $out .= $l; if (strlen($l) < 4 || $l[3] === ' ') break; } return $out; };
    $cmd = function (string $c, string $expect) use ($fp, $read, &$err): bool {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        $r = $read();
        if (strncmp($r, $expect, strlen($expect)) !== 0) { $shown = preg_match('/^(EHLO|AUTH LOGIN$|MAIL FROM|RCPT TO|DATA$)/', $c) ? $c : ($c === '' ? '(greeting)' : '(hidden)'); $err = trim($shown . ' -> ' . $r); return false; }
        return true;
    };
    $user = $cfg['smtp_user'];
    $ok = $cmd('', '220') && $cmd('EHLO efficienthomeimprovements.ca', '250')
        && $cmd('AUTH LOGIN', '334') && $cmd(base64_encode($user), '334') && $cmd(base64_encode(str_replace(' ', '', $cfg['smtp_pass'])), '235')
        && $cmd("MAIL FROM:<$user>", '250');
    foreach ($rcpts as $r) $ok = $ok && $cmd("RCPT TO:<$r>", '25');
    $ok = $ok && $cmd('DATA', '354') && $cmd(preg_replace('/^\./m', '..', $data) . "\r\n.", '250');
    @fwrite($fp, "QUIT\r\n"); fclose($fp);
    return $ok;
}

function field(string $k, int $max): string {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    return mb_substr($v, 0, $max);
}

$lead = [
    'name'    => field('name', 100),
    'phone'   => field('phone', 40),
    'email'   => field('email', 150),
    'city'    => field('city', 80),
    'service' => field('service', 120),
    'message' => field('message', 2000),
    'page'    => field('page', 300),
];

// Honeypot: real visitors never fill this hidden field. Pretend success for bots.
if (field('company', 100) !== '') {
    out(200, ['ok' => true]);
}

$errors = [];
if ($lead['name'] === '')  $errors['name'] = 'Please enter your name.';
if (!preg_match('/\d{3}.*\d{3}.*\d{4}/', $lead['phone'])) $errors['phone'] = 'Please enter a phone number we can call.';
if ($lead['city'] === '')  $errors['city'] = 'Please enter your city.';
if ($lead['email'] !== '' && !filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) $errors['email'] = 'That email address looks incomplete.';
if (preg_match('/https?:\/\//i', $lead['message']) && substr_count(strtolower($lead['message']), 'http') > 2) $errors['message'] = 'Please remove links from your message.';
if ($errors) out(422, ['ok' => false, 'errors' => $errors]);

// Storage outside public_html (deploys replace public_html, this folder survives them).
$store = dirname(__DIR__, 2) . '/ehi-leads';
if (!is_dir($store)) @mkdir($store, 0750, true);
if (!is_dir($store) || !is_writable($store)) {
    $store = sys_get_temp_dir() . '/ehi-leads';
    if (!is_dir($store)) @mkdir($store, 0750, true);
}

// Flood guard per IP (hashed, not stored in clear).
$ipHash = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . 'ehi');
$rateFile = $store . '/sent-' . substr($ipHash, 0, 16) . '.txt';
$now = time();
$hits = array_filter(array_map('intval', @file($rateFile, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > $now - 3600);
if (count($hits) >= MAX_PER_HOUR) out(429, ['ok' => false, 'error' => 'We have already received several requests from this connection in the last hour.']);

$dryRun = ($_POST['dry_run'] ?? '') === '1';
if ($dryRun) out(200, ['ok' => true, 'dry_run' => true, 'would_email' => preg_replace('/^(.).*(@.*)$/', '$1***$2', LEAD_TO), 'mailer' => mail_config() ? 'gmail-smtp' : 'sendmail']);
$hits[] = $now;
@file_put_contents($rateFile, implode("\n", $hits));

// Backup copy (CSV) before emailing.
$csv = $store . '/leads.csv';
$isNew = !file_exists($csv);
if ($fh = @fopen($csv, 'a')) {
    if ($isNew) fputcsv($fh, ['received', 'name', 'phone', 'email', 'city', 'service', 'message', 'page'], ',', '"', '\\');
    fputcsv($fh, array_merge([date('c')], array_values($lead)), ',', '"', '\\');
    fclose($fh);
}

// Email
$from = 'no-reply@efficienthomeimprovements.ca';
$subject = 'New quote request: ' . ($lead['service'] ?: 'HVAC') . ' (' . $lead['city'] . ')';
$lines = [
    'New quote request from the ' . SITE_NAME,
    '',
    'Name:     ' . $lead['name'],
    'Phone:    ' . $lead['phone'],
    'Email:    ' . ($lead['email'] ?: '(not given)'),
    'City:     ' . $lead['city'],
    'Service:  ' . $lead['service'],
    'Page:     ' . $lead['page'],
    '',
    'Message:',
    $lead['message'] ?: '(none)',
    '',
    'Received: ' . date('l, F j, Y g:i a T'),
];
$headers = [
    'From: ' . SITE_NAME . ' <' . $from . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'Cc: ' . LEAD_CC,
    'X-Mailer: EHI-site',
];
if ($lead['email'] !== '') $headers[] = 'Reply-To: ' . str_replace(["\r", "\n"], '', $lead['name']) . ' <' . $lead['email'] . '>';
$encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$cfg = mail_config();
if ($cfg) {
    $smtpHeaders = [
        'Date: ' . date('r'),
        'From: EHI Website Leads <' . $cfg['smtp_user'] . '>',
        'To: ' . LEAD_TO,
        'Cc: ' . LEAD_CC,
        'Subject: ' . $encSubject,
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@efficienthomeimprovements.ca>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    ];
    if ($lead['email'] !== '') $smtpHeaders[] = 'Reply-To: ' . str_replace(["\r", "\n", '<', '>'], '', $lead['name']) . ' <' . $lead['email'] . '>';
    $err = '';
    $sent = smtp_send($cfg, [LEAD_TO, LEAD_CC], implode("\r\n", $smtpHeaders) . "\r\n\r\n" . str_replace("\n", "\r\n", implode("\n", $lines)), $err);
    if (!$sent) @file_put_contents($store . '/mail-errors.log', date('c') . ' ' . $err . "\n", FILE_APPEND);
} else {
    $sent = send_mail(LEAD_TO, $encSubject, implode("\n", $lines), $headers, $from);
}

if (!$wantsJson) {
    header('Location: /thank-you/', true, 303);
    exit;
}
if (!$sent) out(200, ['ok' => false, 'down' => true, 'error' => 'We could not send that just now.']);
out(200, ['ok' => true, 'emailed' => true]);
