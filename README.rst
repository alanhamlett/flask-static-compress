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
      <script type="text/coffeescript" src="file.js"></script>
    {% endcompress %}

Also, initialize the extension inside your Flask app::

    from flask_static_compress import FlaskStaticCompress
    app = Flask(__name__)
    compress = FlaskStaticCompress(app)

All static assets inside a ``compress`` block are compressed into a single file, and the html is updated to use the new file when rendering the template.

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
