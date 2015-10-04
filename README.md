Automated Music Utils
=====================

The first thing I want to say is, yes, I know, the name is totally unimaginative and completely sucks. Hey, I'm a programmer, not a marketing person :).

This project is a command line based set of utilities for dealing with a digital music collection, with an emphasis on minimal user input. It could potentially be of interest to other people who still collect music (i.e. buying vinyl and CDs) and who want to manage and maintain the collection on their own, rather than using something like Spotify. Yes, Spotify and the like are good tools, but they don't necessarily make your own collection obsolete. Believe it or not, there's also music you can't get on them!

I guess at least one part of the appeal of Spotify is that it removes a lot of the tedium associated with having to maintain your own collection; things like renaming files to match the track name, applying ID3 tags, and so on. The intention of this application is to remove that tedium. With a single command, it will rip a CD to WAV, encode those WAVs to MP3 or FLAC, and interface with Discogs to get high quality metadata (the quality of the metadata provided by databases like freedb really sucks) to apply to the MP3s or FLACs.

Installation and Setup
======================
For the time being, this setup is only for Linux.

Eventually, the installation process will be with pip, i.e.:
```
pip install amu
```

The configuration file for AMU is located at ~/.amu_config. This will provide sensible default values for the third party components, but you can edit to suit.

However, this doesn't cover installation and configuration of the third party components.

CD Ripper
---------
AMU uses [Rubyripper](http://wiki.hydrogenaud.io/index.php?title=Rubyripper) to rip CDs. You may ask, why not use EAC? First and foremost, EAC has no command line interface, and that's what this tool is focused on. Secondly, EAC only runs on Windows, and is completely closed source, which kinda sucks. Personally, I don't notice any difference between CDs ripped with EAC or Rubyripper. If you still want to use EAC, you can use it to rip CDs to WAV, then use AMU for everything else.

There are various ways to install Rubyripper, but here's one:
```shell
#!/usr/bin/env bash

apt-get install -y cd-discid cdparanoia
src_path="/opt/rubyripper-0.6.2"
[[ -d "$src_path" ]] && rm -rf $src_path
cd /opt
curl -O https://rubyripper.googlecode.com/files/rubyripper-0.6.2.tar.bz2
tar jxvf rubyripper-0.6.2.tar.bz2
rm rubyripper-0.6.2.tar.bz2
cd $src_path
./configure --enable-lang-all --enable-gtk2 --enable-cli
make install
ln -s $src_path/rubyripper_cli.rb /usr/local/bin/rubyripper_cli
```

It requires some configuration to run from the command line, but the AMU installation will provide this.

MP3 Encoding
------------
The only supported MP3 encoder is [LAME](http://lame.sourceforge.net/). Let's face it, why would you use anything else? Here's one way to install it:

```shell
#!/usr/bin/env bash

cd /tmp
curl -O https://jacderida-software.s3.amazonaws.com/lame-3.99.5.tar.gz
tar -xvf lame-3.99.5.tar.gz
cd lame-3.99.5
./configure
make
make install
rm -rf lame-3.99.5
rm -rf lame-3.99.5.tar.gz
```

By default, AMU uses 'V0' to encode to MP3. This can be modified by editing the AMU configuration file.

FLAC Encoding
-------------
FLAC can generally be installed by using the package manager for your distribution.

By default, AMU uses '-8' as the encoding option, which is the option to provide the most compression. This can be modified by editing the AMU configuration file.

Ripping CDs
===========
With respect to ripping CDs, there are 2 options. Either simply rip the tracks on the CD to WAV, or rip and encode the tracks to MP3 or FLAC in a single step.

To rip the CD to WAV, issue the following command:
```
amu rip
```

This will use Rubyripper to rip the CD tracks to WAV in the current directory. If you want to use something other than the current directory, use the destination override:
```
amu rip --destination=/some/destination
```

To rip the CD to MP3 or FLAC, issue the following command (replace mp3 with flac to encode to FLAC):
```
amu encode cd mp3
```

This command will use Rubyripper to rip the CD, then LAME to encode the WAVs to MP3. The MP3s will be encoded to the current directory. To use a different directory, override the destination:
```
amu encode cd mp3 --destination=/some/destination
```

Both of those encode commands will produce MP3s with no metadata. To produce MP3s that have metadata, supply the Discogs ID for the release:
```
amu encode cd mp3 --discogs-id=123456
```

You can find the ID by looking up the release on discogs; eventually AMU will provide features to help with this.

When you specify the discogs ID, AMU will retrieve the metadata for the release and use that to apply metadata and automatically move the encoded MP3s to a destination that is built based on some values in the configuration file.
