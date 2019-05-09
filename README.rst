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
               
- Landing page provides links to `WordPress plugin search`_, plus a number of
  useful and popular Wordpress plugins (none pre-installed):
   
   - `Yost SEO`_: Optimizes your WordPress blog for search engines and XML
     sitemaps.
   - `NextGEN Gallery`_: Easy to use image gallery with thumbnail & slideshow
     options.
   - `JetPack by WordPress.com`_: Jetpack adds powerful features previously
     only available to WordPress.com users including customization,
     traffic, mobile, content, and performance tools.
   - `WP Super Cache`_: Accelerates your blog by serving 99% of your
     visitors via static HTML files.
   - `Social Media Share Buttons & Icons`_: Promote your content by adding
     links to social sharing and bookmarking sites.
   - `Simple Tags`_: automatically adds tags and related posts to your
     content.
   - `BackupWordPress`_: easily backup your core WordPress tables.
   - `Google Analytics Dashboard for WordPress`_: track visitors, AdSense
     clicks, outgoing links, and search queries.
   - `WP-Polls`_: Adds an easily customizable AJAX poll system to your
     blog.
   - `WP-PageNavi`_: Adds more advanced paging navigation.
   - `Ozh admin dropdown menu`_: Creates a drop down menu with all admin
     links.
   - `Contact Form 7`_: Customizable contact forms supporting AJAX,
     CAPTCHA and Akismet integration.
   - `Seriously Simple Podcasting`_: Simple Podcasting from your WordPress
     site.

- SSL support out of the box.
- `Adminer`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, PHP, MySQL (MariaDB) and Postfix.

See the `WordPress docs`_ for further details (including multisite
howto).

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL: username **root**
-  Adminer: username **adminer**
-  Wordpress: username **admin**


.. _WordPress: https://wordpress.org
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _WordPress plugin search: https://wordpress.org/plugins/
.. _Yost SEO: https://wordpress.org/plugins/wordpress-seo/
.. _NextGEN Gallery: https://wordpress.org/plugins/nextgen-gallery/
.. _JetPack by WordPress.com: https://wordpress.org/plugins/jetpack/
.. _WP Super Cache: https://wordpress.org/plugins/wp-super-cache/
.. _Social Media Share Buttons & Icons: https://wordpress.org/plugins/ultimate-social-media-icons/
.. _Simple Tags: https://wordpress.org/plugins/simple-tags/
.. _BackupWordPress: https://wordpress.org/plugins/backupwordpress/
.. _Google Analytics Dashboard for WordPress: https://wordpress.org/plugins/google-analytics-for-wordpress/
.. _WP-Polls: https://wordpress.org/plugins/wp-polls/
.. _WP-PageNavi: http://wordpress.org/plugins/wp-pagenavi/
.. _Ozh admin dropdown menu: https://wordpress.org/plugins/ozh-admin-drop-down-menu/
.. _Contact Form 7: https://wordpress.org/plugins/contact-form-7/
.. _Seriously Simple Podcasting: https://wordpress.org/plugins/seriously-simple-podcasting/
.. _Adminer: https://www.adminer.org/
.. _WordPress docs: https://www.turnkeylinux.org/docs/wordpress
