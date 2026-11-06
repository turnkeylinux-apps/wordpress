<?php
// Run with turnkey-wp eval-file to exercise WordPress's installed feed parser.
require_once ABSPATH . WPINC . '/class-simplepie.php';

$feed = new SimplePie\SimplePie();
$feed->enable_cache(false);
$feed->set_raw_data(<<<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>TurnKey feed regression</title>
    <link>https://example.invalid/</link>
    <description>Offline dashboard feed fixture</description>
    <item>
      <title>Published article</title>
      <link>https://example.invalid/post</link>
      <guid>turnkey-feed-regression</guid>
      <description>A published article</description>
    </item>
  </channel>
</rss>
XML);

if (!$feed->init()) {
    WP_CLI::error('WordPress feed parsing failed: ' . $feed->error());
}
if ($feed->get_title() !== 'TurnKey feed regression'
    || $feed->get_item_quantity() !== 1
    || $feed->get_item(0)->get_title() !== 'Published article'
    || $feed->get_item(0)->get_link() !== 'https://example.invalid/post') {
    WP_CLI::error('WordPress feed contents did not round-trip');
}
echo "PASS: installed WordPress parser reads dashboard-style RSS\n";
