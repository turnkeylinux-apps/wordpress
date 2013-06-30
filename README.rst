WordPress - Blog Publishing Platform
====================================

`WordPress`_ is a state-of-the-art publishing platform with a focus on
aesthetics, web standards, and usability. It is one of the worlds most
popular blog publishing applications, includes tons of powerful core
functionality, extendable via literally hundreds of plugins, and
supports full theming.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- WordPress configurations:
   
   - Installed from upstream source code to /var/www/wordpress
   - Integrated upgrade mechanism: get WordPress updates straight from
     WordPress's creator Automattic.
   - Uploading of media such as images, videos, etc.
   - Permalinks configuration supported through admin console
     (convenience)
   - Automatic plugin upgrades are supported (convenience).

- Useful and popular Wordpress plugins:
   
   - `Wordpress-SEO`_: Optimizes your WordPress blog for search engines
     and XML sitemaps.
   - `NextGEN Gallery`_: Easy to use image gallery with a Flash
     slideshow option.
   - `WordPress.com Stats`_: Provides detailed visitor statistics,
     optimized for blogging.
   - `WP Super Cache`_: Accelerates your blog by serving 99% of your
     visitors via static HTML files.
   - `Sociable:`_ Promote your content by adding links to social sharing
     and bookmarking sites.
   - `Viper's Video Quicktags`_: easily embed videos from all the major
     web video sites.
   - `Simple Tags`_: automatically adds tags and related posts to your
     content.
   - `WP-DB-Backup`_: easily backup your core WordPress tables.  -
     `Google Analytics for WordPress`_: track visitors, AdSense clicks,
     outgoing links, and search queries.
   - `WP-Polls`_: Adds an easily customizable AJAX poll system to your
     blog.
   - `podPress`_: Adds features to make WordPress the ideal platform for
     hosting a podcast.
   - `WP-PageNavi`_: Adds more advanced paging navigation.
   - `Ozh admin dropdown menu`_: Creates a drop down menu with all admin
     links.
   - `Contact From 7`_: Customizable contact forms supporting AJAX,
     CAPTCHA and Akismet integration.

- SSL support out of the box.
- `PHPMyAdmin`_ administration frontend for MySQL (listening on port
  12322 - uses SSL).
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

See the `WordPress docs`_ for further details (including multisite
howto).

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, phpMyAdmin: username **root**
-  Wordpress: username **admin**


.. _WordPress: http://wordpress.org
.. _TurnKey Core: http://www.turnkeylinux.org/core
.. _Wordpress-SEO: http://yoast.com/wordpress/seo/
.. _NextGEN Gallery: http://wordpress.org/extend/plugins/nextgen-gallery/
.. _WordPress.com Stats: http://wordpress.org/extend/plugins/stats/
.. _WP Super Cache: http://wordpress.org/extend/plugins/wp-super-cache/
.. _`Sociable:`: http://wordpress.org/extend/plugins/sociable/
.. _Viper's Video Quicktags: http://wordpress.org/extend/plugins/vipers-video-quicktags/
.. _Simple Tags: http://wordpress.org/extend/plugins/simple-tags/
.. _WP-DB-Backup: http://wordpress.org/extend/plugins/wp-db-backup/
.. _Google Analytics for WordPress: http://yoast.com/wordpress/google-analytics/
.. _WP-Polls: http://wordpress.org/extend/plugins/wp-polls/
.. _podPress: http://wordpress.org/extend/plugins/podpress/
.. _WP-PageNavi: http://wordpress.org/extend/plugins/wp-pagenavi/
.. _Ozh admin dropdown menu: http://wordpress.org/extend/plugins/ozh-admin-drop-down-menu/
.. _Contact From 7: http://wordpress.org/extend/plugins/contact-form-7/
.. _PHPMyAdmin: http://www.phpmyadmin.net/
.. _WordPress docs: http://www.turnkeylinux.org/docs/wordpress
