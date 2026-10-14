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
const MAX_PER_HOUR = 6;                       // per IP, simple flood guard

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
$rateFile = $store . '/rate-' . substr($ipHash, 0, 16) . '.txt';
$now = time();
$hits = array_filter(array_map('intval', @file($rateFile, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > $now - 3600);
if (count($hits) >= MAX_PER_HOUR) out(429, ['ok' => false, 'error' => 'Too many requests. Please call 1-647-694-5845.']);
$hits[] = $now;
@file_put_contents($rateFile, implode("\n", $hits));

$dryRun = ($_POST['dry_run'] ?? '') === '1';
if ($dryRun) out(200, ['ok' => true, 'dry_run' => true, 'would_email' => preg_replace('/^(.).*(@.*)$/', '$1***$2', LEAD_TO)]);

// Backup copy (CSV) before emailing.
$csv = $store . '/leads.csv';
$isNew = !file_exists($csv);
if ($fh = @fopen($csv, 'a')) {
    if ($isNew) fputcsv($fh, ['received', 'name', 'phone', 'email', 'city', 'service', 'message', 'page']);
    fputcsv($fh, array_merge([date('c')], array_values($lead)));
    fclose($fh);
}

// Email
$host = preg_replace('/[^a-z0-9.\-]/i', '', $_SERVER['HTTP_HOST'] ?? 'efficienthomeimprovements.ca');
$from = 'no-reply@' . preg_replace('/^www\./', '', $host);
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
$sent = @mail(LEAD_TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', implode("\n", $lines), implode("\r\n", $headers), '-f' . $from);

if (!$wantsJson) {
    header('Location: /thank-you/', true, 303);
    exit;
}
out(200, ['ok' => true, 'emailed' => (bool)$sent]);
