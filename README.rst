Flask-Static-Compress
=====================

.. image:: https://travis-ci.org/alanhamlett/flask-static-compress.svg?branch=master
    :target: https://travis-ci.org/alanhamlett/flask-static-compress
    :alt: Tests

.. image:: https://codecov.io/gh/alanhamlett/flask-static-compress/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/alanhamlett/flask-static-compress
    :alt: Coverage

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

The compressed ``a041936b125a3ec4ce9bf7a83130157d.js`` contains both ``app.js`` and ``config.js`` combined for faster page loading.
The file name is calculated based on the contents of ``app.js`` and ``config.js``.
This means any change to your static code is automatically reloaded, or cache-busted, in browsers.

With debug mode turned on, file names and line numbers are preserved while still running the compression flow::

    <script type="text/javascript" src="/static/sdist/93a97ef5491b84db5155916be8f8fd7f-config.js"></script>
    <script type="text/javascript" src="/static/sdist/af77fa42b92bb5a1ef85d9eb773d608e-app.js"></script>

The ``type`` attribute is used to decide which compressor to use for the asset.

Use `offline compression <https://github.com/jaysonsantos/jinja-assets-compressor#offline-compression>`_ for improved performance.

Create `custom compressors <https://github.com/jaysonsantos/jinja-assets-compressor#custom-compressors>`_ to support more types of static files.

For example, to remove trailing commas with `Prettier <https://www.npmjs.com/package/prettier>`_ then compress with `jsmin <https://pypi.python.org/pypi/jsmin>`_::

    import errno
    import subprocess
    from jac.compat import file, u, utf8_encode
    from jac.exceptions import InvalidCompressorError
    from rjsmin import jsmin


    class CustomJavaScriptCompressor(object):
        binary = 'prettier'

        @classmethod
        def compile(cls, content, mimetype='text/less', cwd=None, uri_cwd=None,
                    debug=None):
            if debug:
                return content

            args = ['--no-config', '--ignore-path', '--trailing-comma', 'none']

            args.insert(0, cls.binary)

            try:
                handler = subprocess.Popen(args,
                                           stdout=subprocess.PIPE,
                                           stdin=subprocess.PIPE,
                                           stderr=subprocess.PIPE, cwd=None)
            except OSError as e:
                msg = '{0} encountered an error when executing {1}: {2}'.format(
                    cls.__name__,
                    cls.binary,
                    u(e),
                )
                if e.errno == errno.ENOENT:
                    msg += ' Make sure {0} is in your PATH.'.format(cls.binary)
                raise InvalidCompressorError(msg)

            if isinstance(content, file):
                content = content.read()
            (stdout, stderr) = handler.communicate(input=utf8_encode(content))
            stdout = u(stdout)

            if handler.returncode == 0:
                return jsmin(stdout)
            else:
                raise RuntimeError('Error compressing: %s' % stderr)


    COMPRESSOR_CLASSES = {
        'text/javascript': CustomJavaScriptCompressor,
    }


Configuration
-------------

``COMPRESSOR_ENABLED`` Default: True

``COMPRESSOR_OFFLINE_COMPRESS`` Default: False

``COMPRESSOR_FOLLOW_SYMLINKS`` Default: False

``COMPRESSOR_DEBUG`` Default: False

``COMPRESSOR_OUTPUT_DIR`` Default: app.static_folder + '/sdist'

``COMPRESSOR_STATIC_PREFIX`` Default: app.static_url_path + '/sdist'

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
