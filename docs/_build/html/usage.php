<!DOCTYPE html>


<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>Usage &mdash; PyiUpdater 0.14-dev141210 documentation</title>
    
    <link rel="stylesheet" href="_static/basic.css" type="text/css" />
    <link rel="stylesheet" href="_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootswatch-3.2.0/flatly/bootstrap.min.css" type="text/css" />
    <link rel="stylesheet" href="_static/bootstrap-sphinx.css" type="text/css" />
    
    <script type="text/javascript">
      var DOCUMENTATION_OPTIONS = {
        URL_ROOT:    './',
        VERSION:     '0.14-dev141210',
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
    <link rel="top" title="PyiUpdater 0.14-dev141210 documentation" href="index.php" />
    <link rel="next" title="Architecture" href="architecture.php" />
    <link rel="prev" title="Configuration" href="configuration.php" />
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
        <span class="navbar-text navbar-version pull-left"><b>0.14-dev141210</b></span>
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
<li class="toctree-l1 current"><a class="current reference internal" href="">Usage</a></li>
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
<li><a class="reference internal" href="#">Usage</a><ul>
<li><a class="reference internal" href="#demos">Demos</a></li>
</ul>
</li>
</ul>
</ul>
</li>
              
            
            
              
                
  <li>
    <a href="configuration.php" title="Previous Chapter: Configuration"><span class="glyphicon glyphicon-chevron-left visible-sm"></span><span class="hidden-sm hidden-tablet">&laquo; Configuration</span>
    </a>
  </li>
  <li>
    <a href="architecture.php" title="Next Chapter: Architecture"><span class="glyphicon glyphicon-chevron-right visible-sm"></span><span class="hidden-sm hidden-tablet">Architecture &raquo;</span>
    </a>
  </li>
              
            
            
            
            
              <li class="hidden-sm">
<div id="sourcelink">
  <a href="_sources/usage.txt"
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
      
  <div class="section" id="usage">
<span id="id1"></span><h1>Usage<a class="headerlink" href="#usage" title="Permalink to this headline">¶</a></h1>
<p>After compiling your program with pyinstaller or any freezer that compiles python into a single executable.</p>
<p>Use the Archiver Maker for easy update compression &amp; naming.</p>
<p>Version numbers are in the form of: x.x.x</p>
<p>Check <a class="reference external" href="http://semver.org/">Semantic Versioning</a> for more info</p>
<p>The easiest way to get started quickly is to use to command line tool. After setup is complete you&#8217;ll be ready to start creating updates.</p>
<p>From a terminal:</p>
<div class="highlight-python"><div class="highlight"><pre>$ pyiupdater init
</pre></div>
</div>
<div class="section" id="demos">
<h2>Demos<a class="headerlink" href="#demos" title="Permalink to this headline">¶</a></h2>
<p>So if you opt not to use the cli interface &amp; instead want to integrate PyiUpdater into your build, look below.</p>
<div class="highlight-python"><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre> 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97</pre></div></td><td class="code"><div class="highlight"><pre><span class="kn">import</span> <span class="nn">os</span>

<span class="kn">from</span> <span class="nn">pyi_updater</span> <span class="kn">import</span> <span class="n">PyiUpdater</span><span class="p">,</span> <span class="n">PyiUpdaterConfig</span>


<span class="c"># PyiUpdater handles configuration with simple</span>
<span class="c"># class attributes. They must be in all CAPS.</span>
<span class="c"># to be registered. You may pass in custom</span>
<span class="c"># settings to be used later.</span>
<span class="k">class</span> <span class="nc">DefaultConfig</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span>
    <span class="c"># If left None &quot;PyiUpdater App&quot; will be used</span>
    <span class="n">APP_NAME</span> <span class="o">=</span> <span class="s">&quot;My New App&quot;</span>

    <span class="n">Company_Name</span> <span class="o">=</span> <span class="s">&quot;Acme&quot;</span>

    <span class="c"># Used for verion file signature verification</span>
    <span class="c"># base64 encoded ed25519 key</span>
    <span class="n">PUBLIC_KEY</span> <span class="o">=</span> <span class="s">&#39;zZiCrUaXDwd9pT5FpjoeYCDfO8nBeZGPcpxIkRE2dXg&#39;</span>

    <span class="n">DEV_DATA_DIR</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getcwd</span><span class="p">()</span>
    <span class="c"># Online repository where you host your packages</span>
    <span class="c"># and version file</span>
    <span class="n">UPDATE_URL</span> <span class="o">=</span> <span class="s">&#39;https://acme.com/updates&#39;</span>
    <span class="c"># List of urls to check if version file &amp; update data</span>
    <span class="c"># For each object need the urls will be used in succession</span>
    <span class="c"># until the required object is found</span>
    <span class="n">UPDATE_URLS</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;https://acme.com/updates&#39;</span><span class="p">,</span>
                   <span class="s">&#39;https://mirror.acme.com/updates&#39;</span><span class="p">,</span>
                   <span class="s">&#39;https://acme.amazon.com/updates&#39;</span><span class="p">]</span>
    <span class="n">UPDATE_PATCHES</span> <span class="o">=</span> <span class="bp">True</span>

    <span class="c"># This is a path on the remote server or bucket name</span>
    <span class="c"># on amazon s3</span>
    <span class="n">REMOTE_DIR</span> <span class="o">=</span> <span class="s">&quot;my-new-bucket&quot;</span>

    <span class="c"># The url or ip to remote host server.</span>
    <span class="c"># Mostly for scp uploads</span>
    <span class="n">HOST</span> <span class="o">=</span> <span class="bp">None</span>

    <span class="c"># Username or access ID</span>
    <span class="n">USERNAME</span> <span class="o">=</span> <span class="bp">None</span>

    <span class="c"># Password or path to keyfile if using scp</span>
    <span class="n">PASSWORD</span> <span class="o">=</span> <span class="bp">None</span>


<span class="k">def</span> <span class="nf">main</span><span class="p">():</span>
    <span class="c"># Setting up Config object</span>
    <span class="n">default_config</span> <span class="o">=</span> <span class="n">DefaultConfig</span><span class="p">()</span>

    <span class="c"># Initilizing Main object and configuring</span>
    <span class="c"># in one step</span>
    <span class="n">pyiu_config</span> <span class="o">=</span> <span class="n">PyiUpdaterConfig</span><span class="p">(</span><span class="n">DefaultConfig</span><span class="p">())</span>

    <span class="c"># Can also update config later</span>
    <span class="n">pyiu_config</span><span class="o">.</span><span class="n">update_config</span><span class="p">(</span><span class="n">default_config</span><span class="p">)</span>

    <span class="c"># Initializing PyiUpdater with config info</span>
    <span class="n">pyiu</span> <span class="o">=</span> <span class="n">PyiUpdater</span><span class="p">(</span><span class="n">pyiu_config</span><span class="p">)</span>

    <span class="c"># Can also be Initilized without config</span>
    <span class="n">pyiu</span> <span class="o">=</span> <span class="n">PyiUpdater</span><span class="p">()</span>

    <span class="c"># Then update later with config</span>
    <span class="n">pyiu</span><span class="o">.</span><span class="n">update_config</span><span class="p">(</span><span class="n">pyiu_config</span><span class="p">)</span>

    <span class="c"># Setting up work directories</span>
    <span class="c"># Only need to run once on a new project but it&#39;s</span>
    <span class="c"># ok if ran multipule times</span>
    <span class="n">pyiu</span><span class="o">.</span><span class="n">setup</span><span class="p">()</span>
    <span class="n">pyiu</span><span class="o">.</span><span class="n">make_keys</span><span class="p">()</span>

    <span class="c"># Now place new packages in the folder named</span>
    <span class="c"># &quot;new&quot; in the pyi-data directory</span>
    <span class="c"># Package Archive filename should be in the form</span>
    <span class="c"># AppName-platform-version.zip</span>
    <span class="nb">raw_input</span><span class="p">(</span><span class="s">&#39;Place updates in new folder then press enter.&#39;</span><span class="p">)</span>
    <span class="c"># This updates the version file with the</span>
    <span class="c"># new packages &amp; moves them to the deploy folder.</span>
    <span class="n">pyiu</span><span class="o">.</span><span class="n">process_packages</span><span class="p">()</span>

    <span class="c"># This signs the update manifest &amp; copies it</span>
    <span class="c"># to the deploy folder</span>
    <span class="n">pyiu</span><span class="o">.</span><span class="n">sign_update</span><span class="p">()</span>

    <span class="c"># Load desired uploader</span>
    <span class="k">try</span><span class="p">:</span>
        <span class="n">pyiu</span><span class="o">.</span><span class="n">set_uploader</span><span class="p">(</span><span class="s">&#39;s3&#39;</span><span class="p">)</span>
        <span class="n">pyiu</span><span class="o">.</span><span class="n">upload</span><span class="p">()</span>
    <span class="k">except</span><span class="p">:</span>
        <span class="c"># Make sure you have the requested uploader installed</span>
        <span class="c"># pyiupdater[&#39;s3&#39;] for Amazon S3</span>
        <span class="c"># pyiupdater[&#39;scp&#39;] for server uploads</span>
        <span class="k">print</span> <span class="s">&#39;upload failed&#39;</span>

<span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">&#39;__main__&#39;</span><span class="p">:</span>
    <span class="n">main</span><span class="p">()</span>
</pre></div>
</td></tr></table></div>
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