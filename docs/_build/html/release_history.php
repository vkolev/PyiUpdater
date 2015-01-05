<!DOCTYPE html>


<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>Release History &mdash; PyiUpdater 0.14-dev141453 documentation</title>
    
    <link rel="stylesheet" href="_static/basic.css" type="text/css" />
    <link rel="stylesheet" href="_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootswatch-3.2.0/flatly/bootstrap.min.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootstrap-sphinx.css" type="text/css" />
    
    <script type="text/javascript">
      var DOCUMENTATION_OPTIONS = {
        URL_ROOT:    './',
        VERSION:     '0.14-dev141453',
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
    <link rel="top" title="PyiUpdater 0.14-dev141453 documentation" href="index.php" />
    <link rel="prev" title="License" href="license.php" />
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
        <span class="navbar-text navbar-version pull-left"><b>0.14-dev141453</b></span>
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
<li class="toctree-l1"><a class="reference internal" href="configuration.php">Configuration</a></li>
<li class="toctree-l1"><a class="reference internal" href="usage.php">Usage</a></li>
<li class="toctree-l1"><a class="reference internal" href="architecture.php">Architecture</a></li>
<li class="toctree-l1"><a class="reference internal" href="folder_structure.php">File &amp; Folder Structure</a></li>
<li class="toctree-l1"><a class="reference internal" href="contributing.php">Contributing</a></li>
<li class="toctree-l1"><a class="reference internal" href="api.php">API</a></li>
<li class="toctree-l1"><a class="reference internal" href="license.php">License</a></li>
<li class="toctree-l1 current"><a class="current reference internal" href="">Release History</a></li>
<li class="toctree-l1"><a class="reference internal" href="#if-you-update-to-this-release-do-not-revoke-any-keys-until-you-are-sure-all-clients-are-updated-to-this-version-of-the-framework-if-you-revoke-a-key-it-will-break-the-built-in-migration">If you update to this release, do not revoke any keys until you are sure all clients are updated to this version of the framework. If you revoke a key it will break the built in migration.</a></li>
<li class="toctree-l1"><a class="reference internal" href="#demos-have-been-update-with-the-changes-also-its-very-important-to-make-a-decrypted-copy-of-your-config-file-before-updating">Demos have been update with the changes. Also its very important to make a decrypted copy of your config file before updating.</a></li>
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
<li><a class="reference internal" href="#">Release History</a><ul>
<li><a class="reference internal" href="#v0-14-0-develop">v0.14.0 - Develop</a><ul>
<li><a class="reference internal" href="#backwards-incompatible-release-migration-available">Backwards incompatible release * Migration Available *</a></li>
</ul>
</li>
</ul>
</li>
<li><a class="reference internal" href="#if-you-update-to-this-release-do-not-revoke-any-keys-until-you-are-sure-all-clients-are-updated-to-this-version-of-the-framework-if-you-revoke-a-key-it-will-break-the-built-in-migration">If you update to this release, do not revoke any keys until you are sure all clients are updated to this version of the framework. If you revoke a key it will break the built in migration.</a><ul>
<li><a class="reference internal" href="#v0-13-0-2014-12-27">v0.13.0 - 2014/12/27</a><ul>
<li><a class="reference internal" href="#backwards-incompatible-release">Backwards incompatible release</a></li>
</ul>
</li>
</ul>
</li>
<li><a class="reference internal" href="#demos-have-been-update-with-the-changes-also-its-very-important-to-make-a-decrypted-copy-of-your-config-file-before-updating">Demos have been update with the changes. Also its very important to make a decrypted copy of your config file before updating.</a><ul>
<li><a class="reference internal" href="#v0-12-3-2014-12-7">v0.12.3 - 2014/12/7</a></li>
<li><a class="reference internal" href="#v0-12-2-2014-12-7">v0.12.2 - 2014/12/7</a></li>
<li><a class="reference internal" href="#v0-12-1-2014-12-4">v0.12.1 - 2014/12/4</a></li>
<li><a class="reference internal" href="#v0-12-0-2014-11-29">v0.12.0 - 2014/11/29</a></li>
<li><a class="reference internal" href="#v0-11-0-2014-11-22">v0.11.0 - 2014/11/22</a></li>
<li><a class="reference internal" href="#v0-10-0-2014-11-16">v0.10.0 - 2014/11/16</a></li>
<li><a class="reference internal" href="#v0-9-2-2014-10-19">v0.9.2 - 2014/10/19</a></li>
<li><a class="reference internal" href="#v0-9-1-2014-10-19">v0.9.1 - 2014/10/19</a></li>
<li><a class="reference internal" href="#v0-9-0-2014-10-18">v0.9.0 - 2014/10/18</a></li>
<li><a class="reference internal" href="#v0-8-1-2014-9-3">v0.8.1 - 2014/9/3</a></li>
<li><a class="reference internal" href="#v0-8-0-2014-8-31">v0.8.0 - 2014/8/31</a></li>
<li><a class="reference internal" href="#v0-7-2-2014-8-10">v0.7.2 - 2014/8/10</a></li>
<li><a class="reference internal" href="#v0-7-1-2014-8-10">v0.7.1 - 2014/8/10</a></li>
<li><a class="reference internal" href="#v0-7-2014-8-3">v0.7 - 2014/8/3</a></li>
<li><a class="reference internal" href="#v0-6-0-2014-7-27">v0.6.0 - 2014/7/27</a></li>
</ul>
</li>
</ul>
</ul>
</li>
              
            
            
              
                
  <li>
    <a href="license.php" title="Previous Chapter: License"><span class="glyphicon glyphicon-chevron-left visible-sm"></span><span class="hidden-sm hidden-tablet">&laquo; License</span>
    </a>
  </li>
              
            
            
            
            
              <li class="hidden-sm">
<div id="sourcelink">
  <a href="_sources/release_history.txt"
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
      
  <div class="section" id="release-history">
<h1>Release History<a class="headerlink" href="#release-history" title="Permalink to this headline">¶</a></h1>
<div class="section" id="v0-14-0-develop">
<h2>v0.14.0 - Develop<a class="headerlink" href="#v0-14-0-develop" title="Permalink to this headline">¶</a></h2>
<div class="admonition note">
<p class="first admonition-title">Note</p>
<p class="last">This version is not yet released and is under active development.</p>
</div>
<div class="section" id="backwards-incompatible-release-migration-available">
<h3>Backwards incompatible release * Migration Available *<a class="headerlink" href="#backwards-incompatible-release-migration-available" title="Permalink to this headline">¶</a></h3>
</div>
</div>
</div>
<div class="section" id="if-you-update-to-this-release-do-not-revoke-any-keys-until-you-are-sure-all-clients-are-updated-to-this-version-of-the-framework-if-you-revoke-a-key-it-will-break-the-built-in-migration">
<h1>If you update to this release, do not revoke any keys until you are sure all clients are updated to this version of the framework. If you revoke a key it will break the built in migration.<a class="headerlink" href="#if-you-update-to-this-release-do-not-revoke-any-keys-until-you-are-sure-all-clients-are-updated-to-this-version-of-the-framework-if-you-revoke-a-key-it-will-break-the-built-in-migration" title="Permalink to this headline">¶</a></h1>
<ul>
<li><p class="first">New</p>
<ul>
<li><p class="first">CLI</p>
<ul>
<li><p class="first">Can now revoke signing keys. The number of keys to revoke from oldest.</p>
<div class="highlight-python"><div class="highlight"><pre>$ pyiupdater keys --revoke 1
</pre></div>
</div>
</li>
<li><p class="first">clean command: can remove PyiUpdater data &amp; support file from root dir</p>
</li>
</ul>
</li>
<li><p class="first">PackageHandlder</p>
<ul class="simple">
<li>Added migration command to new key system</li>
</ul>
</li>
</ul>
</li>
<li><p class="first">Updated</p>
<ul class="simple">
<li>CLI<ul>
<li>build command: Fixed naming of exe on windows</li>
<li>init command: can pass &#8211;count with the number of keys to create.</li>
<li>refactored cli code</li>
</ul>
</li>
<li>Client<ul>
<li>Support for multiple public keys verifying</li>
</ul>
</li>
<li>License<ul>
<li>Digital Sapphire Development Team</li>
</ul>
</li>
</ul>
</li>
</ul>
<div class="section" id="v0-13-0-2014-12-27">
<h2>v0.13.0 - 2014/12/27<a class="headerlink" href="#v0-13-0-2014-12-27" title="Permalink to this headline">¶</a></h2>
<div class="section" id="backwards-incompatible-release">
<h3>Backwards incompatible release<a class="headerlink" href="#backwards-incompatible-release" title="Permalink to this headline">¶</a></h3>
</div>
</div>
</div>
<div class="section" id="demos-have-been-update-with-the-changes-also-its-very-important-to-make-a-decrypted-copy-of-your-config-file-before-updating">
<h1>Demos have been update with the changes. Also its very important to make a decrypted copy of your config file before updating.<a class="headerlink" href="#demos-have-been-update-with-the-changes-also-its-very-important-to-make-a-decrypted-copy-of-your-config-file-before-updating" title="Permalink to this headline">¶</a></h1>
<ul class="simple">
<li>Updated<ul>
<li>CLI<ul>
<li>Updated with subcommands</li>
<li>pyiupdater -h</li>
<li>pyiupdater sub_command -h</li>
</ul>
</li>
<li>Client<ul>
<li>Fixed error when version numbers are correct in version file</li>
</ul>
</li>
<li>KeyHandler<ul>
<li>Moved key storage to .pyiupdater folder</li>
</ul>
</li>
<li>PyiUpdater<ul>
<li>Simplified config</li>
</ul>
</li>
</ul>
</li>
<li>Fixed<ul>
<li>PyiUpdater<ul>
<li>Logging when pyi.log is next to Mac .app bundles</li>
</ul>
</li>
</ul>
</li>
<li>Removed<ul>
<li>Client<ul>
<li>Redundant code</li>
</ul>
</li>
<li>FileCrypt<ul>
<li>Passwords for remote locations will need to be set as env vars</li>
</ul>
</li>
<li>PyiUpdater<ul>
<li>Redundant system calls</li>
</ul>
</li>
<li>TUI<ul>
<li>Removed in favor of cli</li>
</ul>
</li>
</ul>
</li>
</ul>
<div class="section" id="v0-12-3-2014-12-7">
<h2>v0.12.3 - 2014/12/7<a class="headerlink" href="#v0-12-3-2014-12-7" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Updated<ul>
<li>Client<ul>
<li>Handling version numbers passed to update_check</li>
</ul>
</li>
</ul>
</li>
<li>Fixed<ul>
<li>Client<ul>
<li>Missing var</li>
</ul>
</li>
<li>PackageHandler<ul>
<li>Incrementing patch number</li>
<li>Trying to move a file that doesn&#8217;t exist</li>
<li>Doing migrate on every run</li>
<li>Getting hash of file that doesn&#8217;t exists</li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-12-2-2014-12-7">
<h2>v0.12.2 - 2014/12/7<a class="headerlink" href="#v0-12-2-2014-12-7" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Updated<ul>
<li>PackageHandler<ul>
<li>Error reporting when calling methods</li>
</ul>
</li>
</ul>
</li>
<li>Fixed<ul>
<li>CLI scripts</li>
</ul>
</li>
<li>Removed<ul>
<li>Some unused code</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-12-1-2014-12-4">
<h2>v0.12.1 - 2014/12/4<a class="headerlink" href="#v0-12-1-2014-12-4" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Fixed<ul>
<li>Migrating to new patch numbering system</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-12-0-2014-11-29">
<h2>v0.12.0 - 2014/11/29<a class="headerlink" href="#v0-12-0-2014-11-29" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Added<ul>
<li>.pyiupdater data directory. Used to keep track of packages &amp; patch numbers.</li>
</ul>
</li>
<li>Updated<ul>
<li>PackageHandler<ul>
<li>Will migrate packages in files directory to safe-to-remove folder.
Now only the most recent package will be kept in files directory for patch creation</li>
</ul>
</li>
</ul>
</li>
<li>Fixed<ul>
<li>Install from setup.py</li>
<li>Failed password retry</li>
</ul>
</li>
<li>Removed</li>
</ul>
</div>
<div class="section" id="v0-11-0-2014-11-22">
<h2>v0.11.0 - 2014/11/22<a class="headerlink" href="#v0-11-0-2014-11-22" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Added<ul>
<li>PyiWrapper<ul>
<li>Spec file support. Spec file will be rejected if onedir mode is specified.</li>
</ul>
</li>
</ul>
</li>
<li>Updated<ul>
<li>Client<ul>
<li>Now each call to update_check returns 1 of 2 update objects. AppUpdate or LibUpdate. The updated objects are nearly identical. The AppUpdate object has a few more methods like restart &amp; extract_restart. Now instead of calling client.download() you will use app_update.download(). Check the demos for more info.</li>
</ul>
</li>
<li>PyiWrapper<ul>
<li>Increased stability of wrapper to better parse args</li>
</ul>
</li>
<li>CLI<ul>
<li>start cli with pyiupdater-cli instead of pyi-cli</li>
</ul>
</li>
</ul>
</li>
<li>Removed<ul>
<li>CLI<ul>
<li>Archiver Utility</li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-10-0-2014-11-16">
<h2>v0.10.0 - 2014/11/16<a class="headerlink" href="#v0-10-0-2014-11-16" title="Permalink to this headline">¶</a></h2>
<ul>
<li><p class="first">Added</p>
<ul>
<li><p class="first">Secure downloading of manifest</p>
</li>
<li><p class="first">Offline update</p>
<ul class="simple">
<li>Upon successful online version manifest signature verification, the version file manifest will be written to the app data folder.</li>
<li>Calls to client.download() will check if update has already been downloaded &amp; return True if the checksum verifies before attempting to download update.</li>
</ul>
</li>
<li><p class="first">Pyinstaller wrapper</p>
<ul>
<li><p class="first">Using the following command compiles your script and archives it ready for file diff and upload:</p>
<div class="highlight-python"><div class="highlight"><pre>$ pyiupdater app.py --app-name=APP --app-version=0.1.0
</pre></div>
</div>
</li>
</ul>
</li>
<li><p class="first">Deprecated Warnings</p>
<ul class="simple">
<li>use client.extract() instead of client.install()</li>
<li>use client.extract_restart() instead of client.install_restart()</li>
</ul>
</li>
</ul>
</li>
<li><p class="first">Updated</p>
<ul class="simple">
<li>URL sanitizing<ul>
<li>Better handling of types passed to config class attributes</li>
</ul>
</li>
</ul>
</li>
<li><p class="first">Fixed</p>
<ul class="simple">
<li>Archiving currently running app<ul>
<li>Will now archive Mac.app apps</li>
</ul>
</li>
</ul>
</li>
<li><p class="first">Removed</p>
<ul class="simple">
<li>Common util functions<ul>
<li>They were added to jms-utils</li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-9-2-2014-10-19">
<h2>v0.9.2 - 2014/10/19<a class="headerlink" href="#v0-9-2-2014-10-19" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Fixed<ul>
<li>Require PyInstaller 2.1.1 for PyiUpdater usage</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-9-1-2014-10-19">
<h2>v0.9.1 - 2014/10/19<a class="headerlink" href="#v0-9-1-2014-10-19" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Added<ul>
<li>Require PyInstaller 2.1.1 for PyiUpdater usage</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-9-0-2014-10-18">
<h2>v0.9.0 - 2014/10/18<a class="headerlink" href="#v0-9-0-2014-10-18" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Added<ul>
<li>Support for multiple update urls</li>
<li>Auto generated client config</li>
<li>ed25529 Update verification<ul>
<li>Using instead of RSA</li>
</ul>
</li>
</ul>
</li>
<li>Updated<ul>
<li>Client updater<ul>
<li>Support Mac GUI app bundles</li>
<li>Better error handling</li>
<li>Less failed application execution when updater
has errors</li>
<li>Patcher<ul>
<li>Now verifies patched update integrity
against version file</li>
</ul>
</li>
</ul>
</li>
<li>Downloader<ul>
<li>Https verification<ul>
<li>on by default</li>
<li>Can disable in config file</li>
<li>VERIFY_SERVER_CERT</li>
</ul>
</li>
<li>Dynamic block resizing</li>
</ul>
</li>
<li>Archive Extraction<ul>
<li>More reliable</li>
</ul>
</li>
<li>Archive creator<ul>
<li>Works with mac GUI apps</li>
</ul>
</li>
<li>Private methods<ul>
<li>Refactored to make testing easier</li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-8-1-2014-9-3">
<h2>v0.8.1 - 2014/9/3<a class="headerlink" href="#v0-8-1-2014-9-3" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Added<ul>
<li>jms-utils</li>
</ul>
</li>
<li>Fixed<ul>
<li>Packaging setup.py installation</li>
</ul>
</li>
<li>Removed<ul>
<li>Unused tests</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-8-0-2014-8-31">
<h2>v0.8.0 - 2014/8/31<a class="headerlink" href="#v0-8-0-2014-8-31" title="Permalink to this headline">¶</a></h2>
<ul>
<li><p class="first">Added</p>
<ul class="simple">
<li>Archive Maker utility<ul>
<li>Makes zip &amp; gzip archives with name, version
and platform in correct format for package handler</li>
</ul>
</li>
<li>Signals<ul>
<li>If you want to run updater in background
thread you can subscribe to signals for
download progress and completion</li>
</ul>
</li>
<li>CLI<ul>
<li>Option to change encryption password</li>
</ul>
</li>
<li>Initial py3 compat</li>
<li>More code comments if you want to get your
hands dirty</li>
<li>Option to enable https verification</li>
</ul>
</li>
<li><p class="first">Updated</p>
<ul class="simple">
<li>Package Handler<ul>
<li>Package metadata parsing is faster. Thanks
to a new &amp; shiny package object.</li>
</ul>
</li>
<li>File Crypt<ul>
<li>Uses simple encryption interface of
simple-crypt. Pycrypto in background.</li>
</ul>
</li>
</ul>
</li>
<li><p class="first">Fixed</p>
<ul>
<li><p class="first">CLI</p>
<ul class="simple">
<li>Initial setup didn&#8217;t save settings
to correct class attributes</li>
</ul>
</li>
<li><p class="first">Client</p>
<ul class="simple">
<li>Parsing of version file</li>
</ul>
</li>
<li><p class="first">Patch creation</p>
<ul>
<li><p class="first">Example:</p>
<p>1.9 &gt; 1.10 was True</p>
<p>1.9 &gt; 1.10 is now False</p>
</li>
</ul>
</li>
</ul>
</li>
<li><p class="first">Removed</p>
<ul class="simple">
<li>Cryptography dependency</li>
<li>License text from individual files</li>
<li>Unused imports</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-7-2-2014-8-10">
<h2>v0.7.2 - 2014/8/10<a class="headerlink" href="#v0-7-2-2014-8-10" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Fixed<ul>
<li>Error on load cli</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-7-1-2014-8-10">
<h2>v0.7.1 - 2014/8/10<a class="headerlink" href="#v0-7-1-2014-8-10" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Added<ul>
<li>Utils<ul>
<li>Utils specific errors</li>
</ul>
</li>
<li>KeyHandler<ul>
<li>Error if DevDataDir not setup</li>
</ul>
</li>
</ul>
</li>
<li>Updated<ul>
<li>Client<ul>
<li>Better parsing of old updates to remove</li>
<li>More error checking</li>
<li>More error reporting</li>
<li>Dynamic creation of archive format</li>
</ul>
</li>
<li>Utils<ul>
<li>Better parsing of dot files for removal</li>
</ul>
</li>
</ul>
</li>
<li>Removed<ul>
<li>Client<ul>
<li>Some old transition code</li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-7-2014-8-3">
<h2>v0.7 - 2014/8/3<a class="headerlink" href="#v0-7-2014-8-3" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Added<ul>
<li>Uploader plugin support</li>
<li>Default S3 &amp; SCP plugins</li>
<li>Support for gzipped archives</li>
</ul>
</li>
<li>Updated<ul>
<li>Menu option handling</li>
</ul>
</li>
<li>Remove<ul>
<li>Upload code for s3 and scp</li>
<li>Unused config options</li>
<li>Redundant upload checks</li>
</ul>
</li>
</ul>
</div>
<div class="section" id="v0-6-0-2014-7-27">
<h2>v0.6.0 - 2014/7/27<a class="headerlink" href="#v0-6-0-2014-7-27" title="Permalink to this headline">¶</a></h2>
<p><strong>* Renamed to PyiUpdater *</strong></p>
<ul class="simple">
<li>Removed<ul>
<li>Old transition code</li>
<li>Binary support<ul>
<li>only pip &amp; src install</li>
</ul>
</li>
</ul>
</li>
</ul>
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
      Last updated on Jan 04, 2015.<br/>
    </p>
  </div>
</footer>
  </body>
</html>