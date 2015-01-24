- Framework

  - Cli

    - add ability to update settings

  - PyiUpdater

    - Clean up version to tuple and vice versa
    - Remove blinker dependency
    - Added callback function, to client,  for download progress
    - More logging

  - Package Handler

    - check make patch | better logging

  - Test Suite

    - Focus on client auto update tests
    - Add more tests!
    - Coverage is lacking

  - Client

    - Change refresh to false as default
    - Check manifest download for duplicate downloading


- Docs

  - Architecture

    -Try to update this information

  - Usage

    - Change up to upload

  -Demos
    - Add comment to show default for company name
    - Make company name all caps
    - Remove all traces of dev_data_dir
    - Make sure demos are consistent with api
    - Make code comment more descriptive for upload.
    - Make note that these are default uploaders

  - PyiUpdater

    - Test if app name with spaces work correctly

  - Tests

    - Add more tests, especially for cli