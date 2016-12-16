Flask-Static-Compress
=====================

Auto-detects your static files for minification, combination, and versioning. Like Django-Compressor for Flask.


Installation
------------

::

    pip install flask-static-compress


Usage
-----

Just wrap your existing css/js with a compress block and Flask-Static-Compress handles the rest::

    {% compress 'css' %}
      <link rel="stylesheet" type="text/sass" href="file.sass">
    {% endcompress %}

    {% compress 'js' %}
      <script type="text/javascript" src="file.js"></script>
    {% endcompress %}

Also, initialize the extension inside your Flask app::

    from flask_static_compress import FlaskStaticCompress
    app = Flask(__name__)
    compress = FlaskStaticCompress(app)

All static assets inside a ``compress`` block are compressed into a single file, and your html is updated to the new path when rendering the template.

For example::

    {% compress 'js' %}
      <script type="text/javascript" src="{{ STATIC_URL }}js/config.js"></script>
      <script type="text/javascript" src="{{ STATIC_URL }}js/app.js"></script>
    {% endcompress %}

Is turned into::

    <script type="text/javascript" src="/static/sdist/a041936b125a3ec4ce9bf7a83130157d.js"></script>

The compressed ``a041936b125a3ec4ce9bf7a83130157d.js`` contains both ``app.js`` and ``config.js`` combined for improved performance.
The file name is calculated based on the contents of ``app.js`` and ``config.js``.
This means any change to your static code is automatically reloaded, or cache-busted, in browsers.

With debug mode turned on, file names and line numbers are preserved while still running the compression flow::

    <script type="text/javascript" src="/static/sdist/93a97ef5491b84db5155916be8f8fd7f-config.js"></script>
    <script type="text/javascript" src="/static/sdist/af77fa42b92bb5a1ef85d9eb773d608e-app.js"></script>

The ``type`` attribute is used to decide which compressor to use for the asset.

Use `offline compression <https://github.com/jaysonsantos/jinja-assets-compressor#offline-compression>`_ for improved performance.

Create `custom compressors <https://github.com/jaysonsantos/jinja-assets-compressor#custom-compressors>`_ to support more types of static files.

Configuration
-------------

``COMPRESSOR_ENABLED`` Default: True

``COMPRESSOR_OFFLINE_COMPRESS`` Default: False

``COMPRESSOR_FOLLOW_SYMLINKS`` Default: False

``COMPRESSOR_DEBUG`` Default: False

``COMPRESSOR_OUTPUT_DIR`` Default: app.static_folder

``COMPRESSOR_STATIC_PREFIX`` Default: app.static_url_path

``COMPRESSOR_CLASSES`` Default::

    [
        'text/css': LessCompressor,
        'text/coffeescript': CoffeeScriptCompressor,
        'text/less': LessCompressor,
        'text/javascript': JavaScriptCompressor,
        'text/sass': SassCompressor,
        'text/scss': SassCompressor,
    ]


Thanks to Jay Santos, creator of `jac <https://github.com/jaysonsantos/jinja-assets-compressor>`_. Flask-Static-Compress is just a wrapper around jac!
