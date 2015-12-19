.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
tdf.siteaccountform
==============================================================================

This Plone add-on provides a form where users could submit personal data to get an account on the website.
The form is linked from the actions menu. It will be send by email to the sites mail account.

Features
--------

Form with the following fields and features:

- name
- first name
- email
- description of the project the account was asked form
- human validation field
- return to root url with a message to the user
- send email to site email account

Examples
--------

This add-on can be seen in action at the following sites:
- templates.libreoffice.org


Documentation
-------------




Translations
------------




Installation
------------

Install tdf.siteaccountform by adding it to your buildout::

    [buildout]

    ...

    eggs =
        tdf.siteaccountform


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/tdf/tdf.siteaccountform/issues
- Source Code: https://github.com/tdf/tdf.siteaccountform
- Documentation:


Support
-------

If you are having issues, please let us know.



License
-------

The project is licensed under the GPLv2.
