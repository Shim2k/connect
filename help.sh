#!/bin/python

Usage: node [options] [ -e script | script.js ] [arguments]
       node debug script.js [arguments]

Options:
  -v, --version         print Node.js version
  -e, --eval script     evaluate script
  -p, --print           evaluate script and print result
  -c, --check           syntax check script without executing
  -i, --interactive     always enter the REPL even if stdin
                        does not appear to be a terminal
  -r, --require         module to preload (option can be repeated)
  --no-deprecation      silence deprecation warnings
  --throw-deprecation   throw an exception anytime a deprecated function is used
  --trace-deprecation   show stack traces on deprecations
  --trace-sync-io       show stack trace when use of sync IO
                        is detected after the first tick
  --track-heap-objects  track heap object allocations for heap snapshots
  --v8-options          print v8 command line options
  --tls-cipher-list=val use an alternative default TLS cipher list
  --icu-data-dir=dir    set ICU data load path to dir
                        (overrides NODE_ICU_DATA)

Environment variables:
NODE_PATH               ':'-separated list of directories

function help {

}
