README
######


NAME

::

    OBJD - object daemon


SYNOPSIS

::

    objctl <cmd> [key=val] [key==val]
    objd


DESCRIPTION

::

    OBJD is a python3 irc bot, it can connect to IRC, fetch and display RSS
    feeds, take todo notes, keep a shopping list and log text. You can also
    copy/paste the service file and run it under systemd for 24/7 presence
    in a IRC channel.

    OBJD users OBJR, containing all the python3 code to program a unix cli
    program, such as disk perisistence for configuration files, event handler
    to handle the client/server connection, code to introspect modules for
    commands, deferred exception handling to not crash on an error, a parser
    to parse commandline options and values, etc.

    OBJD uses OBJX, an module that allows for easy json save//load
    to/from disk of objects. It provides an "clean namespace" Object class
    that only has dunder methods, so the namespace is not cluttered with
    method names. This makes storing and reading to/from json possible.

    OBJD is Public Domain.


USAGE

::

    without any argument the program starts a daemon

    $ objd
    $


    use the objctl program to manage objd



CONFIGURATION

::

    the cfg command is used for configuration of the IRC bot

    $ objctl cfg 
    channel=#objd commands=True nick=objd port=6667 server=localhost

    irc

    $ objctl cfg server=<server>
    $ objctl cfg channel=<channel>
    $ objctl cfg nick=<nick>

    sasl

    $ objctl pwd <nsvnick> <nspass>
    $ objctl cfg password=<frompwd>

    rss

    $ objctl rss <url>
    $ objctl dpl <url> <item1,item2>
    $ objctl rem <url>
    $ objctl nme <url> <name>


COMMANDS

::

    $ objctl cmd
    cfg,cmd,dne,dpl,err,flt,log,mod,mre,nme,pwd,rem,req,res,rss,tdo,thr,tmr


    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    fnd - find objects 
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed
    thr - show the running threads


SYSTEMD

::

    save the following it in /etc/systems/system/objd.service and
    replace "<user>" with the user running pipx

::

    [Unit]
    Description=object daemon
    Requires=network-online.target
    After=network-online.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.objd
    ExecStart=/home/<user>/.local/pipx/venvs/objd/bin/objd
    RemainAfterExit=yes

    [Install]
    WantedBy=default.target

::

    then run this::

    $ pipx ensurepath
    $ mkdir ~/.objd
    $ sudo systemctl enable objd --now

    default channel/server is #objd on localhost


FILES

::

    ~/.objd
    ~/.local/bin/objctl
    ~/.local/bin/objd
    ~/.local/pipx/venvs/objd/


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OBJD is Public Domain.
