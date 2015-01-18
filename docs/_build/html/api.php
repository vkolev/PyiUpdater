<!DOCTYPE html>


<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>API &mdash; PyiUpdater 0.15.1-beta6-4-g9c2a6d7-dirty documentation</title>
    
    <link rel="stylesheet" href="_static/basic.css" type="text/css" />
    <link rel="stylesheet" href="_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootswatch-3.2.0/flatly/bootstrap.min.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootstrap-sphinx.css" type="text/css" />
    
    <script type="text/javascript">
      var DOCUMENTATION_OPTIONS = {
        URL_ROOT:    './',
        VERSION:     '0.15.1-beta6-4-g9c2a6d7-dirty',
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
    <link rel="top" title="PyiUpdater 0.15.1-beta6-4-g9c2a6d7-dirty documentation" href="index.php" />
    <link rel="next" title="License" href="license.php" />
    <link rel="prev" title="Contributing" href="contributing.php" />
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
        <span class="navbar-text navbar-version pull-left"><b>0.15.1-beta6-4-g9c2a6d7-dirty</b></span>
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
<li class="toctree-l1 current"><a class="current reference internal" href="">API</a></li>
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
<li><a class="reference internal" href="#">API</a></li>
</ul>
</ul>
</li>
              
            
            
              
                
  <li>
    <a href="contributing.php" title="Previous Chapter: Contributing"><span class="glyphicon glyphicon-chevron-left visible-sm"></span><span class="hidden-sm hidden-tablet">&laquo; Contributing</span>
    </a>
  </li>
  <li>
    <a href="license.php" title="Next Chapter: License"><span class="glyphicon glyphicon-chevron-right visible-sm"></span><span class="hidden-sm hidden-tablet">License &raquo;</span>
    </a>
  </li>
              
            
            
            
            
              <li class="hidden-sm">
<div id="sourcelink">
  <a href="_sources/api.txt"
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
      
  <div class="section" id="api">
<h1>API<a class="headerlink" href="#api" title="Permalink to this headline">¶</a></h1>
<p>If you want to dive into their documentation, scroll down:</p>
<span class="target" id="module-pyi_updater"></span><dl class="class">
<dt id="pyi_updater.PyiUpdater">
<em class="property">class </em><tt class="descclassname">pyi_updater.</tt><tt class="descname">PyiUpdater</tt><big>(</big><em>config=None</em><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater" title="Permalink to this definition">¶</a></dt>
<dd><p>Processes, signs &amp; uploads updates</p>
<p>Kwargs:</p>
<blockquote>
<div>config (obj): config object</div></blockquote>
<dl class="method">
<dt id="pyi_updater.PyiUpdater.update_config">
<tt class="descname">update_config</tt><big>(</big><em>config</em><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.update_config" title="Permalink to this definition">¶</a></dt>
<dd><p>Updates internal config</p>
<p>Args:</p>
<blockquote>
<div>config (obj): config object</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.PyiUpdater.setup">
<tt class="descname">setup</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.setup" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets up root dir with required PyiUpdater folders</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.PyiUpdater.process_packages">
<tt class="descname">process_packages</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.process_packages" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates hash for updates &amp; adds information about update to
version file</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.PyiUpdater.set_uploader">
<tt class="descname">set_uploader</tt><big>(</big><em>requested_uploader</em><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.set_uploader" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets upload destination</p>
<p>Args:</p>
<blockquote>
<div>requested_uploader (str): upload service. i.e. s3, scp</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.PyiUpdater.upload">
<tt class="descname">upload</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.upload" title="Permalink to this definition">¶</a></dt>
<dd><p>Uploads files in deploy folder</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.PyiUpdater.make_keys">
<tt class="descname">make_keys</tt><big>(</big><em>count</em><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.make_keys" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates signing keys</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.PyiUpdater.sign_update">
<tt class="descname">sign_update</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.sign_update" title="Permalink to this definition">¶</a></dt>
<dd><p>Signs version file with signing key</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.PyiUpdater.get_public_keys">
<tt class="descname">get_public_keys</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.get_public_keys" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns public key</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.PyiUpdater.print_public_key">
<tt class="descname">print_public_key</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.PyiUpdater.print_public_key" title="Permalink to this definition">¶</a></dt>
<dd><p>Prints public key to console</p>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.client"></span><dl class="class">
<dt id="pyi_updater.client.Client">
<em class="property">class </em><tt class="descclassname">pyi_updater.client.</tt><tt class="descname">Client</tt><big>(</big><em>obj=None</em>, <em>refresh=False</em>, <em>test=False</em><big>)</big><a class="headerlink" href="#pyi_updater.client.Client" title="Permalink to this definition">¶</a></dt>
<dd><p>Used on client side to update files</p>
<p>Kwargs:</p>
<blockquote>
<div><p>obj (instance): config object</p>
<p>refresh (bool) Meaning:</p>
<blockquote>
<div><p>True: Refresh update manifest on object initialization</p>
<p>False: Don&#8217;t refresh update manifest on object initialization</p>
</div></blockquote>
</div></blockquote>
<dl class="method">
<dt id="pyi_updater.client.Client.init_app">
<tt class="descname">init_app</tt><big>(</big><em>obj</em>, <em>refresh=True</em>, <em>test=False</em><big>)</big><a class="headerlink" href="#pyi_updater.client.Client.init_app" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets up client with config values from obj</p>
<p>Args:</p>
<blockquote>
<div>obj (instance): config object</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.client.Client.refresh">
<tt class="descname">refresh</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.client.Client.refresh" title="Permalink to this definition">¶</a></dt>
<dd><p>Will download and verify your updates version file.</p>
<p>Proxy method from <tt class="xref py py-meth docutils literal"><span class="pre">_get_update_manifest()</span></tt>.</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.client.Client.update_check">
<tt class="descname">update_check</tt><big>(</big><em>name</em>, <em>version</em><big>)</big><a class="headerlink" href="#pyi_updater.client.Client.update_check" title="Permalink to this definition">¶</a></dt>
<dd><p>Will try to patch binary if all check pass.  IE hash verified
signature verified.  If any check doesn&#8217;t pass then falls back to
full update</p>
<p>Args:</p>
<blockquote>
<div><p>name (str): Name of file to update</p>
<p>version (str): Current version number of file to update</p>
</div></blockquote>
<p>Returns:</p>
<blockquote>
<div><p>(bool) Meanings:</p>
<blockquote>
<div><p>True - Update Successful</p>
<p>False - Update Failed</p>
</div></blockquote>
</div></blockquote>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.client.updates"></span><dl class="class">
<dt id="pyi_updater.client.updates.LibUpdate">
<em class="property">class </em><tt class="descclassname">pyi_updater.client.updates.</tt><tt class="descname">LibUpdate</tt><big>(</big><em>data</em><big>)</big><a class="headerlink" href="#pyi_updater.client.updates.LibUpdate" title="Permalink to this definition">¶</a></dt>
<dd><p>Used to update library files used by an application</p>
<p>Args:</p>
<blockquote>
<div>data (dict): Info dict</div></blockquote>
<dl class="method">
<dt id="pyi_updater.client.updates.LibUpdate.download">
<tt class="descname">download</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.client.updates.LibUpdate.download" title="Permalink to this definition">¶</a></dt>
<dd><p>Will download the package update that was referenced
with check update.</p>
<p>Proxy method for <tt class="xref py py-meth docutils literal"><span class="pre">_patch_update()</span></tt> &amp; <tt class="xref py py-meth docutils literal"><span class="pre">_full_update()</span></tt>.</p>
<p>Returns:</p>
<blockquote>
<div><p>(bool) Meanings:</p>
<blockquote>
<div><p>True - Download successful</p>
<p>False - Download failed</p>
</div></blockquote>
</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.client.updates.LibUpdate.extract">
<tt class="descname">extract</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.client.updates.LibUpdate.extract" title="Permalink to this definition">¶</a></dt>
<dd><p>Will extract archived update and leave in update folder.
If updating a lib you can take over from there. If updating
an app this call should be followed by <tt class="xref py py-meth docutils literal"><span class="pre">restart()</span></tt> to
complete update.</p>
<p>Proxy method for <tt class="xref py py-meth docutils literal"><span class="pre">_extract_update()</span></tt>.</p>
<p>Returns:</p>
<blockquote>
<div><p>(bool) Meanings:</p>
<blockquote>
<div><p>True - Install successful</p>
<p>False - Install failed</p>
</div></blockquote>
</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.client.updates.LibUpdate.install">
<tt class="descname">install</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.client.updates.LibUpdate.install" title="Permalink to this definition">¶</a></dt>
<dd><p>DEPRECATED! Proxy method for <a class="reference internal" href="#pyi_updater.client.updates.LibUpdate.extract" title="pyi_updater.client.updates.LibUpdate.extract"><tt class="xref py py-meth docutils literal"><span class="pre">extract()</span></tt></a>.</p>
</dd></dl>

</dd></dl>

<dl class="class">
<dt id="pyi_updater.client.updates.AppUpdate">
<em class="property">class </em><tt class="descclassname">pyi_updater.client.updates.</tt><tt class="descname">AppUpdate</tt><big>(</big><em>data</em><big>)</big><a class="headerlink" href="#pyi_updater.client.updates.AppUpdate" title="Permalink to this definition">¶</a></dt>
<dd><p>Used to update library files used by an application</p>
<p>Args:</p>
<blockquote>
<div>data (dict): Info dict</div></blockquote>
<dl class="method">
<dt id="pyi_updater.client.updates.AppUpdate.extract_restart">
<tt class="descname">extract_restart</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.client.updates.AppUpdate.extract_restart" title="Permalink to this definition">¶</a></dt>
<dd><p>Will extract the update, overwrite the current app,
then restart the app using the updated binary.</p>
<p>On windows Proxy method for <tt class="xref py py-meth docutils literal"><span class="pre">_extract_update()</span></tt> &amp;
<tt class="xref py py-meth docutils literal"><span class="pre">_win_overwrite_app_restart()</span></tt></p>
<p>On unix Proxy method for <tt class="xref py py-meth docutils literal"><span class="pre">_extract_update()</span></tt>,
<tt class="xref py py-meth docutils literal"><span class="pre">_overwrite_app()</span></tt> &amp; <tt class="xref py py-meth docutils literal"><span class="pre">_restart()</span></tt></p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.client.updates.AppUpdate.install_restart">
<tt class="descname">install_restart</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.client.updates.AppUpdate.install_restart" title="Permalink to this definition">¶</a></dt>
<dd><p>DEPRECATED!  Proxy method for <a class="reference internal" href="#pyi_updater.client.updates.AppUpdate.extract_restart" title="pyi_updater.client.updates.AppUpdate.extract_restart"><tt class="xref py py-meth docutils literal"><span class="pre">extract_restart()</span></tt></a>.</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.client.updates.AppUpdate.restart">
<tt class="descname">restart</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.client.updates.AppUpdate.restart" title="Permalink to this definition">¶</a></dt>
<dd><p>Will overwrite old binary with updated binary and
restart using the updated binary. Not supported on windows.</p>
<p>Proxy method for <tt class="xref py py-meth docutils literal"><span class="pre">_overwrite_app()</span></tt> &amp; <tt class="xref py py-meth docutils literal"><span class="pre">_restart()</span></tt>.</p>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.client.utils"></span><dl class="function">
<dt id="pyi_updater.client.utils.get_mac_dot_app_dir">
<tt class="descclassname">pyi_updater.client.utils.</tt><tt class="descname">get_mac_dot_app_dir</tt><big>(</big><em>directory</em><big>)</big><a class="headerlink" href="#pyi_updater.client.utils.get_mac_dot_app_dir" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns parent directory of mac .app</p>
<p>Args:</p>
<blockquote>
<div>directory (str): Current directory</div></blockquote>
<p>Returns:</p>
<blockquote>
<div>(str): Parent directory of mac .app</div></blockquote>
</dd></dl>

<dl class="function">
<dt id="pyi_updater.client.utils.get_highest_version">
<tt class="descclassname">pyi_updater.client.utils.</tt><tt class="descname">get_highest_version</tt><big>(</big><em>name</em>, <em>plat</em>, <em>easy_data</em><big>)</big><a class="headerlink" href="#pyi_updater.client.utils.get_highest_version" title="Permalink to this definition">¶</a></dt>
<dd><p>Parses version file and returns the highest version number.</p>
<p>Args:</p>
<blockquote>
<div><p>name (str): name of file to search for updates</p>
<p>easy_data (dict): data file to search</p>
</div></blockquote>
<p>Returns:</p>
<blockquote>
<div>(str) Highest version number</div></blockquote>
</dd></dl>

<dl class="function">
<dt id="pyi_updater.client.utils.get_filename">
<tt class="descclassname">pyi_updater.client.utils.</tt><tt class="descname">get_filename</tt><big>(</big><em>name</em>, <em>version</em>, <em>platform</em>, <em>easy_data</em><big>)</big><a class="headerlink" href="#pyi_updater.client.utils.get_filename" title="Permalink to this definition">¶</a></dt>
<dd><p>Gets full filename for given name &amp; version combo</p>
<p>Args:</p>
<blockquote>
<div><p>name (str): name of file to get full filename for</p>
<p>version (str): version of file to get full filename for</p>
<p>easy_data (dict): data file to search</p>
</div></blockquote>
<p>Returns:</p>
<blockquote>
<div>(str) Filename with extension</div></blockquote>
</dd></dl>

<span class="target" id="module-pyi_updater.config"></span><dl class="class">
<dt id="pyi_updater.config.Loader">
<em class="property">class </em><tt class="descclassname">pyi_updater.config.</tt><tt class="descname">Loader</tt><a class="headerlink" href="#pyi_updater.config.Loader" title="Permalink to this definition">¶</a></dt>
<dd><p>Loads &amp;  saves config file</p>
<dl class="method">
<dt id="pyi_updater.config.Loader.load_config">
<tt class="descname">load_config</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.config.Loader.load_config" title="Permalink to this definition">¶</a></dt>
<dd><p>Load config file from file system</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.config.Loader.save_config">
<tt class="descname">save_config</tt><big>(</big><em>obj</em><big>)</big><a class="headerlink" href="#pyi_updater.config.Loader.save_config" title="Permalink to this definition">¶</a></dt>
<dd><p>Saves config file to file system</p>
<p>Args:</p>
<blockquote>
<div>obj (obj): config object</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.config.Loader.write_config_py">
<tt class="descname">write_config_py</tt><big>(</big><em>obj</em><big>)</big><a class="headerlink" href="#pyi_updater.config.Loader.write_config_py" title="Permalink to this definition">¶</a></dt>
<dd><p>Writes client config to client_config.py</p>
<p>Args:</p>
<blockquote>
<div>obj (obj): config object</div></blockquote>
</dd></dl>

</dd></dl>

<dl class="class">
<dt id="pyi_updater.config.PyiUpdaterConfig">
<em class="property">class </em><tt class="descclassname">pyi_updater.config.</tt><tt class="descname">PyiUpdaterConfig</tt><big>(</big><em>obj=None</em><big>)</big><a class="headerlink" href="#pyi_updater.config.PyiUpdaterConfig" title="Permalink to this definition">¶</a></dt>
<dd><p>Works exactly like a dict but provides ways to fill it from files
or special dictionaries.  There are two common patterns to populate the
config.</p>
<p>You can define the configuration options in the
module that calls <a class="reference internal" href="#pyi_updater.config.PyiUpdaterConfig.from_object" title="pyi_updater.config.PyiUpdaterConfig.from_object"><tt class="xref py py-meth docutils literal"><span class="pre">from_object()</span></tt></a>.  It is also possible to tell it
to use the same module and with that provide the configuration values
just before the call.</p>
<p>Loading from modules, only uppercase keys are added to the config.
This makes it possible to use lowercase values in the config file for
temporary values that are not added to the config or to define the config
keys in the same file that implements the application.</p>
<dl class="method">
<dt id="pyi_updater.config.PyiUpdaterConfig.from_object">
<tt class="descname">from_object</tt><big>(</big><em>obj</em><big>)</big><a class="headerlink" href="#pyi_updater.config.PyiUpdaterConfig.from_object" title="Permalink to this definition">¶</a></dt>
<dd><p>Updates the values from the given object</p>
<p>Args:</p>
<blockquote>
<div>obj (instance): Object with config attributes</div></blockquote>
<p>Objects are classes.</p>
<p>Just the uppercase variables in that object are stored in the config.
Example usage:</p>
<div class="highlight-python"><div class="highlight"><pre><span class="kn">from</span> <span class="nn">yourapplication</span> <span class="kn">import</span> <span class="n">default_config</span>
<span class="n">app</span><span class="o">.</span><span class="n">config</span><span class="o">.</span><span class="n">from_object</span><span class="p">(</span><span class="n">default_config</span><span class="p">())</span>
</pre></div>
</div>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.config.PyiUpdaterConfig.update_config">
<tt class="descname">update_config</tt><big>(</big><em>obj</em><big>)</big><a class="headerlink" href="#pyi_updater.config.PyiUpdaterConfig.update_config" title="Permalink to this definition">¶</a></dt>
<dd><p>Proxy method to update self</p>
<p>Args:</p>
<blockquote>
<div>obj (instance): config object</div></blockquote>
</dd></dl>

</dd></dl>

<dl class="class">
<dt id="pyi_updater.config.SetupConfig">
<em class="property">class </em><tt class="descclassname">pyi_updater.config.</tt><tt class="descname">SetupConfig</tt><a class="headerlink" href="#pyi_updater.config.SetupConfig" title="Permalink to this definition">¶</a></dt>
<dd><p>Default config object</p>
</dd></dl>

<span class="target" id="module-pyi_updater.downloader"></span><dl class="class">
<dt id="pyi_updater.downloader.FileDownloader">
<em class="property">class </em><tt class="descclassname">pyi_updater.downloader.</tt><tt class="descname">FileDownloader</tt><big>(</big><em>filename</em>, <em>urls</em>, <em>hexdigest=None</em>, <em>verify=True</em><big>)</big><a class="headerlink" href="#pyi_updater.downloader.FileDownloader" title="Permalink to this definition">¶</a></dt>
<dd><p>The FileDownloader object downloads files to memory and
verifies their hash.  If hash is verified data is either
written to disk to returned to calling object</p>
<p>Args:</p>
<blockquote>
<div><p>filename (str): The name of file to download</p>
<p>urls (list): List of urls to use for file download</p>
</div></blockquote>
<p>Kwargs:</p>
<blockquote>
<div><p>hexdigest (str): The hash of the file to download</p>
<p>verify (bool) Meaning:</p>
<blockquote>
<div><p>True: Verify https connection</p>
<p>False: Don&#8217;t verify https connection</p>
</div></blockquote>
</div></blockquote>
<dl class="method">
<dt id="pyi_updater.downloader.FileDownloader.download_verify_write">
<tt class="descname">download_verify_write</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.downloader.FileDownloader.download_verify_write" title="Permalink to this definition">¶</a></dt>
<dd><p>Downloads file then verifies against provided hash
If hash verfies then writes data to disk</p>
<p>Returns:</p>
<blockquote>
<div><p>(bool) Meanings:</p>
<blockquote>
<div><p>True - Hash verified</p>
<p>False - Hash not verified</p>
</div></blockquote>
</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.downloader.FileDownloader.download_verify_return">
<tt class="descname">download_verify_return</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.downloader.FileDownloader.download_verify_return" title="Permalink to this definition">¶</a></dt>
<dd><p>Downloads file to memory, checks against provided hash
If matched returns binary data</p>
<p>Returns:</p>
<blockquote>
<div><p>(data) Meanings:</p>
<blockquote>
<div><p>Data - If everything verified</p>
<p>None - If any verification didn&#8217;t pass</p>
</div></blockquote>
</div></blockquote>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.exceptions"></span><dl class="exception">
<dt id="pyi_updater.exceptions.STDError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">STDError</tt><big>(</big><em>msg</em>, <em>tb=None</em>, <em>expected=False</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.STDError" title="Permalink to this definition">¶</a></dt>
<dd><p>Extends exceptions to show added message if error isn&#8217;t expected.</p>
<p>Args:</p>
<blockquote>
<div>msg (str): error message</div></blockquote>
<p>Kwargs:</p>
<blockquote>
<div><p>tb (obj): is the original traceback so that it can be printed.</p>
<p>expected (bool):</p>
<blockquote>
<div><p>Meaning:</p>
<blockquote>
<div><p>True - Report issue msg not shown</p>
<p>False - Report issue msg shown</p>
</div></blockquote>
</div></blockquote>
</div></blockquote>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.ArchiverError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">ArchiverError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.ArchiverError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Archiver exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.ClientError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">ClientError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.ClientError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Client exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.ConfigError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">ConfigError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.ConfigError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Config exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.FileDownloaderError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">FileDownloaderError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.FileDownloaderError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for FileDownloader exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.KeyHandlerError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">KeyHandlerError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.KeyHandlerError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for KeyHandler exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.PackageError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">PackageError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.PackageError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Package exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.PackageHandlerError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">PackageHandlerError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.PackageHandlerError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for PackageHandler exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.PatcherError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">PatcherError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.PatcherError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Patcher exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.PyiUpdaterError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">PyiUpdaterError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.PyiUpdaterError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Framework exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.UpdaterError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">UpdaterError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.UpdaterError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Updater exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.UploaderError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">UploaderError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.UploaderError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Uploader exceptions</p>
</dd></dl>

<dl class="exception">
<dt id="pyi_updater.exceptions.UtilsError">
<em class="property">exception </em><tt class="descclassname">pyi_updater.exceptions.</tt><tt class="descname">UtilsError</tt><big>(</big><em>*args</em>, <em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.exceptions.UtilsError" title="Permalink to this definition">¶</a></dt>
<dd><p>Raised for Utils exceptions</p>
</dd></dl>

<span class="target" id="module-pyi_updater.key_handler"></span><dl class="class">
<dt id="pyi_updater.key_handler.KeyHandler">
<em class="property">class </em><tt class="descclassname">pyi_updater.key_handler.</tt><tt class="descname">KeyHandler</tt><big>(</big><em>app=None</em><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.KeyHandler" title="Permalink to this definition">¶</a></dt>
<dd><p>KeyHanlder object is used to manage keys used for signing updates</p>
<p>Kwargs:</p>
<blockquote>
<div>app (obj): Config object to get config values from</div></blockquote>
<dl class="method">
<dt id="pyi_updater.key_handler.KeyHandler.init_app">
<tt class="descname">init_app</tt><big>(</big><em>obj</em><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.KeyHandler.init_app" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets up client with config values from obj</p>
<p>Args:</p>
<blockquote>
<div>obj (instance): config object</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.KeyHandler.make_keys">
<tt class="descname">make_keys</tt><big>(</big><em>count=3</em><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.KeyHandler.make_keys" title="Permalink to this definition">¶</a></dt>
<dd><p>Makes public and private keys for signing and verification</p>
<p>Kwargs:</p>
<blockquote>
<div>count (bool): The number of keys to create.</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.KeyHandler.sign_update">
<tt class="descname">sign_update</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.KeyHandler.sign_update" title="Permalink to this definition">¶</a></dt>
<dd><p>Signs version file with private key</p>
<p>Proxy method for <tt class="xref py py-meth docutils literal"><span class="pre">_add_sig()</span></tt></p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.KeyHandler.get_public_key">
<tt class="descname">get_public_key</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.KeyHandler.get_public_key" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns (object): Public Key</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.KeyHandler.get_public_keys">
<tt class="descname">get_public_keys</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.KeyHandler.get_public_keys" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns (object): Public Key</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.KeyHandler.print_public_key">
<tt class="descname">print_public_key</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.KeyHandler.print_public_key" title="Permalink to this definition">¶</a></dt>
<dd><p>Prints public key data to console</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.KeyHandler.print_public_keys">
<tt class="descname">print_public_keys</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.KeyHandler.print_public_keys" title="Permalink to this definition">¶</a></dt>
<dd><p>Prints public key data to console</p>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.key_handler.keydb"></span><dl class="class">
<dt id="pyi_updater.key_handler.keydb.KeyDB">
<em class="property">class </em><tt class="descclassname">pyi_updater.key_handler.keydb.</tt><tt class="descname">KeyDB</tt><big>(</big><em>data_dir</em>, <em>load=False</em><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.keydb.KeyDB" title="Permalink to this definition">¶</a></dt>
<dd><p>Handles finding, sorting, getting meta-data, moving packages.</p>
<p>Kwargs:</p>
<blockquote>
<div><p>data_dir (str): Path to directory containing key.db</p>
<p>load (bool):</p>
<blockquote>
<div><p>Meaning:</p>
<blockquote>
<div><p>True: Load db on initialization</p>
<p>False: Do not load db on initialization</p>
</div></blockquote>
</div></blockquote>
</div></blockquote>
<dl class="method">
<dt id="pyi_updater.key_handler.keydb.KeyDB.add_key">
<tt class="descname">add_key</tt><big>(</big><em>public</em>, <em>private</em>, <em>key_type='ed25519'</em><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.keydb.KeyDB.add_key" title="Permalink to this definition">¶</a></dt>
<dd><p>Adds key pair to database</p>
<p>Args:</p>
<blockquote>
<div><p>public (str): Public key</p>
<p>private (str): Private key</p>
<p>key_type (str): The type of key pair. Default ed25519</p>
</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.keydb.KeyDB.get_public_keys">
<tt class="descname">get_public_keys</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.keydb.KeyDB.get_public_keys" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns a list of all valid public keys</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.keydb.KeyDB.get_private_keys">
<tt class="descname">get_private_keys</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.keydb.KeyDB.get_private_keys" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns a list of all valid private keys</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.keydb.KeyDB.get_revoked_key">
<tt class="descname">get_revoked_key</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.keydb.KeyDB.get_revoked_key" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns most recent revoked key pair</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.keydb.KeyDB.revoke_key">
<tt class="descname">revoke_key</tt><big>(</big><em>count=1</em><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.keydb.KeyDB.revoke_key" title="Permalink to this definition">¶</a></dt>
<dd><p>Revokes key pair</p>
<p>Args:</p>
<blockquote>
<div>count (int): The number of keys to revoke. Oldest first</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.keydb.KeyDB.load">
<tt class="descname">load</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.keydb.KeyDB.load" title="Permalink to this definition">¶</a></dt>
<dd><p>Loads data from key.db</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.key_handler.keydb.KeyDB.save">
<tt class="descname">save</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.key_handler.keydb.KeyDB.save" title="Permalink to this definition">¶</a></dt>
<dd><p>Saves data to key.db</p>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.package_handler"></span><dl class="class">
<dt id="pyi_updater.package_handler.PackageHandler">
<em class="property">class </em><tt class="descclassname">pyi_updater.package_handler.</tt><tt class="descname">PackageHandler</tt><big>(</big><em>app=None</em><big>)</big><a class="headerlink" href="#pyi_updater.package_handler.PackageHandler" title="Permalink to this definition">¶</a></dt>
<dd><p>Handles finding, sorting, getting meta-data, moving packages.</p>
<p>Kwargs:</p>
<blockquote>
<div>app (instance): Config object</div></blockquote>
<dl class="method">
<dt id="pyi_updater.package_handler.PackageHandler.init_app">
<tt class="descname">init_app</tt><big>(</big><em>obj</em><big>)</big><a class="headerlink" href="#pyi_updater.package_handler.PackageHandler.init_app" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets up client with config values from obj</p>
<p>Args:</p>
<blockquote>
<div>obj (instance): config object</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.package_handler.PackageHandler.setup">
<tt class="descname">setup</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.package_handler.PackageHandler.setup" title="Permalink to this definition">¶</a></dt>
<dd><p>Creates working directories &amp; loads json files.</p>
<p>Proxy method for <tt class="xref py py-meth docutils literal"><span class="pre">_setup_work_dirs()</span></tt> &amp; <tt class="xref py py-meth docutils literal"><span class="pre">_load_version_file()</span></tt></p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.package_handler.PackageHandler.process_packages">
<tt class="descname">process_packages</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.package_handler.PackageHandler.process_packages" title="Permalink to this definition">¶</a></dt>
<dd><p>Gets a list of updates to process.  Adds the name of an
update to the version file if not already present.  Processes
all packages.  Updates the version file meta-data. Then writes
version file back to disk.</p>
<p>Proxy method for <tt class="xref py py-meth docutils literal"><span class="pre">_get_package_list()</span></tt>,
<tt class="xref py py-meth docutils literal"><span class="pre">_make_patches()</span></tt>, <tt class="xref py py-meth docutils literal"><span class="pre">_add_patches_to_packages()</span></tt>,
<tt class="xref py py-meth docutils literal"><span class="pre">_update_version_file()</span></tt>,
<tt class="xref py py-meth docutils literal"><span class="pre">_write_json_to_file()</span></tt> &amp; <tt class="xref py py-meth docutils literal"><span class="pre">_move_packages()</span></tt>.</p>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.package_handler.package"></span><dl class="class">
<dt id="pyi_updater.package_handler.package.Patch">
<em class="property">class </em><tt class="descclassname">pyi_updater.package_handler.package.</tt><tt class="descname">Patch</tt><big>(</big><em>patch_info</em><big>)</big><a class="headerlink" href="#pyi_updater.package_handler.package.Patch" title="Permalink to this definition">¶</a></dt>
<dd><p>Holds information for patch file.</p>
<p>Args:</p>
<blockquote>
<div>patch_info (dict): patch information</div></blockquote>
</dd></dl>

<dl class="class">
<dt id="pyi_updater.package_handler.package.Package">
<em class="property">class </em><tt class="descclassname">pyi_updater.package_handler.package.</tt><tt class="descname">Package</tt><big>(</big><em>filename</em><big>)</big><a class="headerlink" href="#pyi_updater.package_handler.package.Package" title="Permalink to this definition">¶</a></dt>
<dd><p>Holds information of update file.</p>
<p>Args:</p>
<blockquote>
<div>filename (str): name of update file</div></blockquote>
<dl class="method">
<dt id="pyi_updater.package_handler.package.Package.extract_info">
<tt class="descname">extract_info</tt><big>(</big><em>package</em><big>)</big><a class="headerlink" href="#pyi_updater.package_handler.package.Package.extract_info" title="Permalink to this definition">¶</a></dt>
<dd><p>Gets version number, platform &amp; hash for package.</p>
<p>Args:</p>
<blockquote>
<div>package (str): filename</div></blockquote>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.patcher"></span><dl class="class">
<dt id="pyi_updater.patcher.Patcher">
<em class="property">class </em><tt class="descclassname">pyi_updater.patcher.</tt><tt class="descname">Patcher</tt><big>(</big><em>**kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.patcher.Patcher" title="Permalink to this definition">¶</a></dt>
<dd><p>Downloads, verifies, and patches binaries</p>
<p>Kwargs:</p>
<blockquote>
<div><p>name (str): Name of binary to patch</p>
<p>json_data (dict): Info dict with all package meta data</p>
<p>current_version (str): Version number of currently installed binary</p>
<p>highest_version (str): Newest version available</p>
<p>update_folder (str): Path to update folder to place updated binary in</p>
<p>update_urls (list): List of urls to use for file download</p>
<p>verify (bool) Meaning:</p>
<blockquote>
<div><p>True: Verify https connection</p>
<p>False: Don&#8217;t verify https connection</p>
</div></blockquote>
</div></blockquote>
<dl class="method">
<dt id="pyi_updater.patcher.Patcher.start">
<tt class="descname">start</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.patcher.Patcher.start" title="Permalink to this definition">¶</a></dt>
<dd><p>Starts patching process</p>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.utils"></span><dl class="class">
<dt id="pyi_updater.utils.bsdiff4_py">
<em class="property">class </em><tt class="descclassname">pyi_updater.utils.</tt><tt class="descname">bsdiff4_py</tt><a class="headerlink" href="#pyi_updater.utils.bsdiff4_py" title="Permalink to this definition">¶</a></dt>
<dd><p>Pure-python version of bsdiff4 module that can only patch, not diff.</p>
<p>By providing a pure-python fallback, we don&#8217;t force frozen apps to
bundle the bsdiff module in order to make use of patches.  Besides,
the patch-applying algorithm is very simple.</p>
</dd></dl>

<dl class="function">
<dt id="pyi_updater.utils.make_archive">
<tt class="descclassname">pyi_updater.utils.</tt><tt class="descname">make_archive</tt><big>(</big><em>name</em>, <em>version</em>, <em>target</em><big>)</big><a class="headerlink" href="#pyi_updater.utils.make_archive" title="Permalink to this definition">¶</a></dt>
<dd><p>Used to make archives of file or dir. Zip on windows and tar.gz
on all other platforms</p>
<dl class="docutils">
<dt>Args:</dt>
<dd><p class="first">name - Name of app. Used to create final archive name</p>
<p>version - Version of app. Used to create final archive name</p>
<p class="last">target - name of actual target file or dir.</p>
</dd>
<dt>Returns:</dt>
<dd>(str) - name of archive</dd>
</dl>
</dd></dl>

<span class="target" id="module-pyi_updater.uploader"></span><dl class="class">
<dt id="pyi_updater.uploader.Uploader">
<em class="property">class </em><tt class="descclassname">pyi_updater.uploader.</tt><tt class="descname">Uploader</tt><big>(</big><em>app=None</em><big>)</big><a class="headerlink" href="#pyi_updater.uploader.Uploader" title="Permalink to this definition">¶</a></dt>
<dd><p>Uploads updates to configured servers.  SSH, SFTP, S3
Will automatically pick the correct uploader depending on
what is configured thorough the config object</p>
<p>Sets up client with config values from obj</p>
<blockquote>
<div><p>Args:</p>
<blockquote>
<div>obj (instance): config object</div></blockquote>
</div></blockquote>
<dl class="method">
<dt id="pyi_updater.uploader.Uploader.init_app">
<tt class="descname">init_app</tt><big>(</big><em>obj</em><big>)</big><a class="headerlink" href="#pyi_updater.uploader.Uploader.init_app" title="Permalink to this definition">¶</a></dt>
<dd><p>Sets up client with config values from obj</p>
<p>Args:</p>
<blockquote>
<div>obj (instance): config object</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.uploader.Uploader.upload">
<tt class="descname">upload</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.uploader.Uploader.upload" title="Permalink to this definition">¶</a></dt>
<dd><p>Proxy function that calls the upload method on the received uploader
Only calls the upload method if an uploader is set.</p>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.uploader.Uploader.set_uploader">
<tt class="descname">set_uploader</tt><big>(</big><em>requested_uploader</em><big>)</big><a class="headerlink" href="#pyi_updater.uploader.Uploader.set_uploader" title="Permalink to this definition">¶</a></dt>
<dd><p>Returns an uploader object. 1 of S3, SCP, SFTP.
SFTP uploaders not supported at this time.</p>
<p>Args:</p>
<blockquote>
<div>requested_uploader (string): Either s3 or scp</div></blockquote>
<p>Returns:</p>
<blockquote>
<div>object (instance): Uploader object</div></blockquote>
</dd></dl>

</dd></dl>

<span class="target" id="module-pyi_updater.uploader.common"></span><dl class="class">
<dt id="pyi_updater.uploader.common.BaseUploader">
<em class="property">class </em><tt class="descclassname">pyi_updater.uploader.common.</tt><tt class="descname">BaseUploader</tt><a class="headerlink" href="#pyi_updater.uploader.common.BaseUploader" title="Permalink to this definition">¶</a></dt>
<dd><p>Base Uploader.  All uploaders should subclass
this base class</p>
<dl class="method">
<dt id="pyi_updater.uploader.common.BaseUploader.init">
<tt class="descname">init</tt><big>(</big><em>**Kwargs</em><big>)</big><a class="headerlink" href="#pyi_updater.uploader.common.BaseUploader.init" title="Permalink to this definition">¶</a></dt>
<dd><p>Used to initialize your plugin with username,
password, file list, remote_dir/bucket &amp; host.
self._connect should be called after you grab all the
info you need.</p>
<p>Kwargs:</p>
<blockquote>
<div><p>file_list (list): List of files to upload</p>
<p>host (str): Either ip or domain name of remote servers</p>
<p>bucket_name/remote_dir (str): Remote location for update</p>
<p>remote_dir (str): The directory on remote server to upload files to</p>
<p>username/aws_access_id (str): login for service</p>
<p>password/ssh_key_file/aws_secret_key (str): login for service</p>
</div></blockquote>
</dd></dl>

<dl class="method">
<dt id="pyi_updater.uploader.common.BaseUploader.upload">
<tt class="descname">upload</tt><big>(</big><big>)</big><a class="headerlink" href="#pyi_updater.uploader.common.BaseUploader.upload" title="Permalink to this definition">¶</a></dt>
<dd><p>Uploads all files in file_list</p>
</dd></dl>

</dd></dl>

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