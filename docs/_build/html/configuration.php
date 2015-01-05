<!DOCTYPE html>


<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>Configuration &mdash; PyiUpdater 0.15.0-dirty documentation</title>
    
    <link rel="stylesheet" href="_static/basic.css" type="text/css" />
    <link rel="stylesheet" href="_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootswatch-3.2.0/flatly/bootstrap.min.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootstrap-sphinx.css" type="text/css" />
    
    <script type="text/javascript">
      var DOCUMENTATION_OPTIONS = {
        URL_ROOT:    './',
        VERSION:     '0.15.0-dirty',
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
    <link rel="top" title="PyiUpdater 0.15.0-dirty documentation" href="index.php" />
    <link rel="next" title="Usage" href="usage.php" />
    <link rel="prev" title="Installation" href="installation.php" />
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
        <span class="navbar-text navbar-version pull-left"><b>0.15.0-dirty</b></span>
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
<li class="toctree-l1"><a class="reference internal" href="installation.php">Installation</a></li>
<li class="toctree-l1 current"><a class="current reference internal" href="">Configuration</a></li>
<li class="toctree-l1"><a class="reference internal" href="usage.php">Usage</a></li>
<li class="toctree-l1"><a class="reference internal" href="architecture.php">Architecture</a></li>
<li class="toctree-l1"><a class="reference internal" href="folder_structure.php">File &amp; Folder Structure</a></li>
<li class="toctree-l1"><a class="reference internal" href="contributing.php">Contributing</a></li>
<li class="toctree-l1"><a class="reference internal" href="api.php">API</a></li>
<li class="toctree-l1"><a class="reference internal" href="license.php">License</a></li>
<li class="toctree-l1"><a class="reference internal" href="release_history.php">Release History</a></li>
<li class="toctree-l1"><a class="reference internal" href="release_history.php#if-you-update-to-this-release-do-not-revoke-any-keys-until-you-are-sure-all-clients-are-updated-to-this-version-of-the-framework-if-you-revoke-a-key-it-will-break-the-built-in-migration">If you update to this release, do not revoke any keys until you are sure all clients are updated to this version of the framework. If you revoke a key it will break the built in migration.</a></li>
<li class="toctree-l1"><a class="reference internal" href="release_history.php#demos-have-been-update-with-the-changes-also-its-very-important-to-make-a-decrypted-copy-of-your-config-file-before-updating">Demos have been update with the changes. Also its very important to make a decrypted copy of your config file before updating.</a></li>
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
<li><a class="reference internal" href="#">Configuration</a></li>
</ul>
</ul>
</li>
              
            
            
              
                
  <li>
    <a href="installation.php" title="Previous Chapter: Installation"><span class="glyphicon glyphicon-chevron-left visible-sm"></span><span class="hidden-sm hidden-tablet">&laquo; Installation</span>
    </a>
  </li>
  <li>
    <a href="usage.php" title="Next Chapter: Usage"><span class="glyphicon glyphicon-chevron-right visible-sm"></span><span class="hidden-sm hidden-tablet">Usage &raquo;</span>
    </a>
  </li>
              
            
            
            
            
              <li class="hidden-sm">
<div id="sourcelink">
  <a href="_sources/configuration.txt"
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
      
  <div class="section" id="configuration">
<span id="id1"></span><h1>Configuration<a class="headerlink" href="#configuration" title="Permalink to this headline">¶</a></h1>
<table border="1" class="docutils">
<colgroup>
<col width="35%" />
<col width="65%" />
</colgroup>
<tbody valign="top">
<tr class="row-odd"><td><tt class="docutils literal"><span class="pre">APP_NAME</span></tt></td>
<td>(str) Name of your app. Used with
COMPANY_NAME to create an update cache dir on end user system.</td>
</tr>
<tr class="row-even"><td><tt class="docutils literal"><span class="pre">COMPANY_NAME</span></tt></td>
<td>(str) Company or your name.  Used with
APP_NAME to create an update cache dir on end user system.</td>
</tr>
<tr class="row-odd"><td><tt class="docutils literal"><span class="pre">DEV_DATA_DIR</span></tt></td>
<td>(str) Full path to directory where
pyiupdater will keep work files. i.e signing
keys, src file for patch creation, etc.</td>
</tr>
<tr class="row-even"><td><tt class="docutils literal"><span class="pre">PUBLIC_KEY</span></tt></td>
<td>(tuple) Used on client side for
authentication</td>
</tr>
<tr class="row-odd"><td><tt class="docutils literal"><span class="pre">UPDATE_URL</span></tt></td>
<td>(str) Where clients search for updates
- * Deprecated! You can put a single url
in the list of UPDATE_URLS *</td>
</tr>
<tr class="row-even"><td><tt class="docutils literal"><span class="pre">UPDATE_URLS</span></tt></td>
<td>(list) A list of url(s) where a client will
look for needed update objects.</td>
</tr>
<tr class="row-odd"><td><tt class="docutils literal"><span class="pre">UPDATE_PATCHES</span></tt></td>
<td>(bool) Enable/disable creation of patch
updates</td>
</tr>
<tr class="row-even"><td><tt class="docutils literal"><span class="pre">REMOTE_DIR</span></tt></td>
<td>(str) Remote directory/Bucket name to place
update files</td>
</tr>
<tr class="row-odd"><td><tt class="docutils literal"><span class="pre">HOST</span></tt></td>
<td>(str) Remote host to connect to for server
uploads</td>
</tr>
<tr class="row-even"><td><tt class="docutils literal"><span class="pre">USERNAME</span></tt></td>
<td>(str) Username/API Key for uploading updates</td>
</tr>
</tbody>
</table>
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
      Last updated on Jan 04, 2015.<br/>
    </p>
  </div>
</footer>
  </body>
</html>