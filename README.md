Automated Music Utils
=====================

The first thing I want to say is, yes, I know, the name is totally unimaginative and completely sucks. Hey, I'm a programmer, not a marketing person :).

This project is a command line based set of utilities for dealing with a digital music collection, with an emphasis on minimal user input. It could potentially be of interest to other people who still collect music (i.e. buying vinyl and CDs) and who want to manage and maintain the collection on their own, rather than using something like Spotify. Yes, Spotify is cool, but it doesn't necessarily make your own collection obsolete, and believe it or not, there's also music you can't get on it!

I guess at least one part of the appeal of Spotify is that it removes a lot of the tedium associated with having to maintain your own collection; things like renaming files to match the track name, applying ID3 tags and so on. The intention of this application is to remove that tedium. With a single command, it will rip a CD to WAV, encode those WAVs to MP3 or FLAC, and interface with Discogs to get high quality metadata (the quality of the metadata provided by databases like freedb really sucks) to apply to the MP3s or FLACs.

When installed, to encode a CD to MP3, I'm going to be able to do this:

    amu search "artist name"
    amu encode cd mp3 --discogsid=12345

The first command will help me obtain the Discogs release ID (which I can't really get automatically), and after I have that ID, I can use it to encode the CD to MP3.

So far, I've finished CD ripping and encoding WAV to MP3.
