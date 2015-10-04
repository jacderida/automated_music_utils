Automated Music Utils
=====================

The first thing I want to say is, yes, I know, the name is totally unimaginative and completely sucks. Hey, I'm a programmer, not a marketing person :).

This project is a command line based set of utilities for dealing with a digital music collection, with an emphasis on minimal user input. It could potentially be of interest to other people who still collect music (i.e. buying vinyl and CDs) and who want to manage and maintain the collection on their own, rather than using something like Spotify. Yes, Spotify and the like are good tools, but they don't necessarily make your own collection obsolete. Believe it or not, there's also music you can't get on them!

I guess at least one part of the appeal of Spotify is that it removes a lot of the tedium associated with having to maintain your own collection; things like renaming files to match the track name, applying ID3 tags, and so on. The intention of this application is to remove that tedium. With a single command, it will rip a CD to WAV, encode those WAVs to MP3 or FLAC, and interface with Discogs to get high quality metadata (the quality of the metadata provided by databases like freedb really sucks) to apply to the MP3s or FLACs.

Installation and Setup
======================
Eventually the installation process will be with pip, i.e.:
```
pip install amu
```

CD Ripper
---------
AMU uses [Rubyripper](http://wiki.hydrogenaud.io/index.php?title=Rubyripper) to rip CDs. You may be ask, why not use EAC? First and foremost, EAC has no command line interface, and that's what this tool is focused on. Secondly, EAC only runs on Windows, and is completely closed source, which kinda sucks. Personally, I don't notice any difference between CDs ripped with EAC or Rubyripper. If you still want to use EAC, you can use it to rip CDs to WAV, then use AMU for everything else.

There are various ways to install Rubyripper, but here is one way:
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
