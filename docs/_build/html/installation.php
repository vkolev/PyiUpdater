<!DOCTYPE html>


<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>Installation &mdash; PyiUpdater 0.16-b1-dirty documentation</title>
    
    <link rel="stylesheet" href="_static/basic.css" type="text/css" />
    <link rel="stylesheet" href="_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootswatch-3.2.0/flatly/bootstrap.min.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootstrap-sphinx.css" type="text/css" />
    
    <script type="text/javascript">
      var DOCUMENTATION_OPTIONS = {
        URL_ROOT:    './',
        VERSION:     '0.16-b1-dirty',
        COLLAPSE_INDEX: false,
        FILE_SUFFIX: '.php',
        HAS_SOURCE:  true
      };
    </script>
    <script type="text/javascript" src="_static/jquery.js"></script>
    <script type="text/javascript" src="_static/underscore.js"></script>
    <script type="text/javascript" src="_static/doctools.js"></script>
    <script type="text/javascript" src="_static/js/jquery-1.11.0.min.js"></script>
    <script type="text/javascript" src="_static/js/jquery-fix.js"></script>
    <script type="text/javascript" src="_static/bootstrap-3.2.0/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="_static/bootstrap-sphinx.js"></script>
    <link rel="top" title="PyiUpdater 0.16-b1-dirty documentation" href="index.php" />
    <link rel="next" title="Configuration" href="configuration.php" />
    <link rel="prev" title="Downloads" href="downloads.php" />
<meta charset='utf-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1'>
<meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1'>
<meta name="apple-mobile-web-app-capable" content="yes">

  </head>
  <body>

  <div id="navbar" class="navbar navbar-default navbar-fixed-top">
    <div class="container">
      <div class="navbar-header">
        <!-- .btn-navbar is used as the toggle for collapsed navbar content -->
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".nav-collapse">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="index.php">
          PyiUpdater</a>
        <span class="navbar-text navbar-version pull-left"><b>0.16-b1-dirty</b></span>
      </div>

        <div class="collapse navbar-collapse nav-collapse">
          <ul class="nav navbar-nav">
            
            
              <li class="dropdown globaltoc-container">
  <a role="button"
     id="dLabelGlobalToc"
     data-toggle="dropdown"
     data-target="#"
     href="index.php">Site <b class="caret"></b></a>
  <ul class="dropdown-menu globaltoc"
      role="menu"
      aria-labelledby="dLabelGlobalToc"><ul class="current">
<li class="toctree-l1"><a class="reference internal" href="downloads.php">Downloads</a></li>
<li class="toctree-l1 current"><a class="current reference internal" href="">Installation</a></li>
<li class="toctree-l1"><a class="reference internal" href="configuration.php">Configuration</a></li>
<li class="toctree-l1"><a class="reference internal" href="usage.php">Usage</a></li>
<li class="toctree-l1"><a class="reference internal" href="architecture.php">Architecture</a></li>
<li class="toctree-l1"><a class="reference internal" href="folder_structure.php">File &amp; Folder Structure</a></li>
<li class="toctree-l1"><a class="reference internal" href="contributing.php">Contributing</a></li>
<li class="toctree-l1"><a class="reference internal" href="api.php">API</a></li>
<li class="toctree-l1"><a class="reference internal" href="license.php">License</a></li>
<li class="toctree-l1"><a class="reference internal" href="release_history.php">Release History</a></li>
<li class="toctree-l1"><a class="reference internal" href="release_history.php#changelog">Changelog</a></li>
</ul>
</ul>
</li>
              
                <li class="dropdown">
  <a role="button"
     id="dLabelLocalToc"
     data-toggle="dropdown"
     data-target="#"
     href="#">Page <b class="caret"></b></a>
  <ul class="dropdown-menu localtoc"
      role="menu"
      aria-labelledby="dLabelLocalToc"><ul>
<li><a class="reference internal" href="#">Installation</a></li>
</ul>
</ul>
</li>
              
            
            
              
                
  <li>
    <a href="downloads.php" title="Previous Chapter: Downloads"><span class="glyphicon glyphicon-chevron-left visible-sm"></span><span class="hidden-sm hidden-tablet">&laquo; Downloads</span>
    </a>
  </li>
  <li>
    <a href="configuration.php" title="Next Chapter: Configuration"><span class="glyphicon glyphicon-chevron-right visible-sm"></span><span class="hidden-sm hidden-tablet">Configuration &raquo;</span>
    </a>
  </li>
              
            
            
            
            
              <li class="hidden-sm">
<div id="sourcelink">
  <a href="_sources/installation.txt"
     rel="nofollow">Source</a>
</div></li>
            
          </ul>

          
            
<form class="navbar-form navbar-right" action="search.php" method="get">
 <div class="form-group">
  <input type="text" name="q" class="form-control" placeholder="Search" />
 </div>
  <input type="hidden" name="check_keywords" value="yes" />
  <input type="hidden" name="area" value="default" />
</form>
          
        </div>
    </div>
  </div>

<div class="container">
  <div class="row">
    <div class="col-md-12">
      
  <div class="section" id="installation">
<span id="id1"></span><h1>Installation<a class="headerlink" href="#installation" title="Permalink to this headline">¶</a></h1>
<p>PyiUpdater depends on a few external libraries: <a class="reference external" href="https://pypi.python.org/pypi/appdirs/">appdirs</a>, <a class="reference external" href="https://pypi.python.org/pypi/blinker">blinker</a>, <a class="reference external" href="http://aws.amazon.com/sdkforpython/">boto</a>,  <a class="reference external" href="https://github.com/ilanschnell/bsdiff4">bsdiff4</a>, <a class="reference external" href="https://pypi.python.org/pypi/certifi">certifi</a>, <a class="reference external" href="https://pypi.python.org/pypi/ed25519">ed25519</a>, <a class="reference external" href="https://pypi.python.org/pypi/JMS-Utils">jms_utils</a> , <a class="reference external" href="https://github.com/pyinstaller/pyinstaller">pyinstaller</a>, <a class="reference external" href="https://pypi.python.org/pypi/simple-pbkdf2">simple_pbkdf2</a>, <a class="reference external" href="https://pypi.python.org/pypi/six">six</a>, <a class="reference external" href="https://pypi.python.org/pypi/stevedore">stevedore</a> &amp; <a class="reference external" href="https://pypi.python.org/pypi/urllib3">urllib3</a>. Bsdiff4 is only required to make patches, not to apply them.  These libraries are not documented here.</p>
<p>So how do you get all that on your computer quickly?</p>
<p>Install from pip:</p>
<div class="highlight-python"><div class="highlight"><pre>$ pip install PyiUpdater
</pre></div>
</div>
<p>S3 &amp; SCP upload plugins are available with:</p>
<div class="highlight-python"><div class="highlight"><pre>$ pip install PyiUpdater[s3]

$ pip install PyiUpdater[scp]
</pre></div>
</div>
<p>If you want the bleeding edge download a pre-release version. WARNING! -&gt; pre released version may not work as expected:</p>
<div class="highlight-python"><div class="highlight"><pre>$ pip install PyiUpdater --pre
</pre></div>
</div>
</div>


    </div>
      
  </div>
</div>
<footer class="footer">
  <div class="container">
    <p class="pull-right">
      <a href="#">Back to top</a>
      
    </p>
    <p>
        &copy; Copyright 2014, Digital Sapphire.<br/>
      Last updated on Jan 17, 2015.<br/>
    </p>
  </div>
</footer>
  </body>
</html>