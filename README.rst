WordPress - Blog Publishing Platform
====================================

`WordPress`_ is a state-of-the-art publishing platform with a focus on
aesthetics, web standards, and usability. It is one of the worlds most
popular blog publishing applications, includes tons of powerful core
functionality, extendable via literally thousands of plugins, and
supports full theming.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- WordPress configurations:
   
   - Installed from upstream source code to /var/www/wordpress
   - Integrated upgrade mechanism: get WordPress updates straight from
     WordPress' creator Automattic.
   - Uploading of media such as images, videos, etc.
   - Permalinks configuration supported through admin console
     (convenience)
   - Automatic minor updates are supported (convenience).
   - **Security note**: Major updates to wordpress may require
     supervision so they **ARE NOT** configured to install automatically.
     See upstream documentation for updating Wordpress major releases.
               
- Useful and popular Wordpress plugins:
   
   - `Wordpress-SEO`_: Optimizes your WordPress blog for search engines
     and XML sitemaps.
   - `NextGEN Gallery`_: Easy to use image gallery with a Flash
     slideshow option.
   - `JetPack for WordPress`_: Jetpack adds powerful features previously
     only available to WordPress.com users including customization,
     traffic, mobile, content, and performance tools.
   - `WP Super Cache`_: Accelerates your blog by serving 99% of your
     visitors via static HTML files.
   - `Ultimate Social Media Icons`_: Promote your content by adding links to social sharing
     and bookmarking sites.
   - `Simple Tags`_: automatically adds tags and related posts to your
     content.
   - `BackupWordPress`_: easily backup your core WordPress tables.
   - `Google Analytics for WordPress`_: track visitors, AdSense clicks,
     outgoing links, and search queries.
   - `WP-Polls`_: Adds an easily customizable AJAX poll system to your
     blog.
   - `WP-PageNavi`_: Adds more advanced paging navigation.
   - `Ozh admin dropdown menu`_: Creates a drop down menu with all admin
     links.
   - `Contact From 7`_: Customizable contact forms supporting AJAX,
     CAPTCHA and Akismet integration.
   - `WP-Update-Notifier`_: Sends email to notify you if there are any updates for your
     WordPress site. Can notify about core, plugin and theme updates.
   - `Seriously Simple Podcasting`_: Simple Podcasting from your WordPress site.

- SSL support out of the box.
- `Adminer`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

See the `WordPress docs`_ for further details (including multisite
howto).

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, Adminer: username **root**
-  Wordpress: username **admin**


.. _WordPress: http://wordpress.org
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _Wordpress-SEO: http://yoast.com/wordpress/seo/
.. _NextGEN Gallery: http://wordpress.org/extend/plugins/nextgen-gallery/
.. _JetPack for WordPress: http://wordpress.org/extend/plugins/jetpack/
.. _WP Super Cache: http://wordpress.org/extend/plugins/wp-super-cache/
.. _Ultimate Social Media Icons: http://wordpress.org/extend/plugins/ultimate-social-media-icons/
.. _Simple Tags: http://wordpress.org/extend/plugins/simple-tags/
.. _BackupWordPress: http://wordpress.org/extend/plugins/backupwordpress/
.. _Google Analytics for WordPress: http://yoast.com/wordpress/google-analytics/
.. _WP-Polls: http://wordpress.org/extend/plugins/wp-polls/
.. _WP-Update-Notifier: http://wordpress.org/extend/plugins/wp-updates-notifier/
.. _WP-PageNavi: http://wordpress.org/extend/plugins/wp-pagenavi/
.. _Ozh admin dropdown menu: http://wordpress.org/extend/plugins/ozh-admin-drop-down-menu/
.. _Contact From 7: http://wordpress.org/extend/plugins/contact-form-7/
.. _Seriously Simple Podcasting: http://wordpress.org/extend/plugins/seriously-simple-podcasting/
.. _Adminer: http://www.adminer.org/
.. _WordPress docs: https://www.turnkeylinux.org/docs/wordpress
