<?php
/** Real WordPress mail/reset acceptance, invoked only by WP-CLI on a disposable fixture. */
if (!defined('WP_CLI') || !WP_CLI || count($args) !== 2) {
    throw new RuntimeException('Run with WP-CLI and an action plus private configuration path.');
}
list($action, $path) = $args;
$config = json_decode(file_get_contents($path), true, 512, JSON_THROW_ON_ERROR);
if (empty($config['disposable']) || !preg_match('/^appmail_qa_[a-z0-9_]+$/', $config['username'])) {
    throw new RuntimeException('An explicit disposable appmail fixture is required.');
}
$state_path = $path . '.state';
function appmail_output($value) { echo json_encode($value, JSON_THROW_ON_ERROR) . "\n"; }
function appmail_remove($state) {
    $user = get_user_by('id', $state['id']);
    if ($user && $user->user_login !== $state['username']) {
        throw new RuntimeException('Fixture ownership changed.');
    }
    require_once ABSPATH . 'wp-admin/includes/user.php';
    if ($user) { wp_delete_user($user->ID); }
}
if ($action === 'begin') {
    if (username_exists($config['username']) || email_exists($config['recipient'])) {
        throw new RuntimeException('Fixture user already exists.');
    }
    if (get_option('admin_email') !== $config['admin_recipient']) {
        throw new RuntimeException('Configure a controlled administrator mailbox before this test.');
    }
    $id = wp_create_user($config['username'], wp_generate_password(32, true, true), $config['recipient']);
    if (is_wp_error($id)) { throw new RuntimeException('Fixture registration failed.'); }
    $state = array('id' => $id, 'username' => $config['username']);
    file_put_contents($state_path, json_encode($state, JSON_THROW_ON_ERROR));
    chmod($state_path, 0600);
    try {
        wp_new_user_notification($id, null, 'both');
        $reset = retrieve_password($config['username']);
        if (is_wp_error($reset) || !$reset) { throw new RuntimeException('Password reset mail failed.'); }
    } catch (Throwable $error) {
        appmail_remove($state);
        unlink($state_path);
        throw $error;
    }
    appmail_output(array('registered' => true, 'reset_requested' => true, 'user_id' => $id));
} elseif ($action === 'finish' || $action === 'cleanup') {
    $state = json_decode(file_get_contents($state_path), true, 512, JSON_THROW_ON_ERROR);
    if ($state['username'] !== $config['username']) { throw new RuntimeException('Fixture mismatch.'); }
    try {
        if ($action === 'finish') {
            $user = check_password_reset_key($config['key'], $config['username']);
            if (is_wp_error($user) || $user->ID !== $state['id']) {
                throw new RuntimeException('Received reset key was not accepted.');
            }
            $password = wp_generate_password(32, true, true);
            reset_password($user, $password);
            $authenticated = wp_authenticate($config['username'], $password);
            if (is_wp_error($authenticated) || $authenticated->ID !== $state['id']) {
                throw new RuntimeException('New password did not authenticate.');
            }
            if (!is_wp_error(check_password_reset_key($config['key'], $config['username']))) {
                throw new RuntimeException('Reset key could be replayed.');
            }
            appmail_output(array('received_reset_accepted' => true,
                'new_password_authenticated' => true, 'reset_replay_rejected' => true));
        }
    } finally {
        appmail_remove($state);
        unlink($state_path);
    }
} else {
    throw new RuntimeException('Unknown action.');
}
