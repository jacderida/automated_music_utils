import os
import shutil
import subprocess
import tempfile
import uuid
from amu import utils
from amu.config import ConfigurationError
from mutagen import File
from mutagen.flac import FLAC, Picture
from mutagen.id3 import APIC, COMM, ID3, ID3NoHeaderError, PictureType, TALB, TCON, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK
from PIL import Image

class TaggerError(Exception):
    def __init__(self, message):
        super(TaggerError, self).__init__(message)
        self.message = message

class LameEncoder(object):
    def __init__(self, config_provider):
        self._config_provider = config_provider

    def encode(self, source, destination):
        if not source:
            raise ValueError('A value must be supplied for the source')
        if not destination:
            raise ValueError('A value must be supplied for the destination')
        if not os.path.exists(source):
            raise ConfigurationError('The source to encode does not exist')
        if os.path.isdir(source):
            raise ConfigurationError('The source should not be a directory')
        subprocess_args = [
            self._config_provider.get_lame_path(),
            self._config_provider.get_lame_encoding_setting(),
            source,
            destination
        ]
        print u'[encode] Running lame with {0}'.format(subprocess_args)
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines_iterator = iter(popen.stdout.readline, '')
        for line in lines_iterator:
            if line:
                print u'[encode] {0}'.format(line.strip().decode('utf-8'))

class FlacEncoder(object):
    def __init__(self, config_provider):
        self._config_provider = config_provider

    def encode(self, source, destination):
        if not source:
            raise ValueError('A value must be supplied for the source')
        if not destination:
            raise ValueError('A value must be supplied for the destination')
        if not os.path.exists(source):
            raise ConfigurationError('The source to encode does not exist')
        if os.path.isdir(source):
            raise ConfigurationError('The source should not be a directory')
        subprocess_args = [
            self._config_provider.get_flac_path(),
            self._config_provider.get_flac_encoding_setting(),
            source,
            '--output-name={0}'.format(destination)
        ]
        print u'[encode] Running flac with {0}'.format(subprocess_args)
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines_iterator = iter(popen.stdout.readline, '')
        for line in lines_iterator:
            if line:
                print u'[encode] {0}'.format(line.strip().decode('utf-8'))

    def decode(self, source, destination):
        if not source:
            raise ValueError('A value must be supplied for the source')
        if not destination:
            raise ValueError('A value must be supplied for the destination')
        if not os.path.exists(source):
            raise ConfigurationError('The source to decode does not exist')
        if os.path.isdir(source):
            raise ConfigurationError('The source should not be a directory')
        subprocess_args = [
            self._config_provider.get_flac_path(),
            self._config_provider.get_flac_decode_setting(),
            source,
            '--output-name={0}'.format(destination)
        ]
        print u'[decode] Running flac with {0}'.format(subprocess_args)
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines_iterator = iter(popen.stdout.readline, '')
        for line in lines_iterator:
            if line:
                print u'[decode] {0}'.format(line.strip().decode('utf-8'))

class RubyRipperCdRipper(object):
    def __init__(self, config_provider):
        self._config_provider = config_provider

    def rip_cd(self, destination):
        if not destination:
            raise ConfigurationError('A destination must be provided for the CD rip')
        expanded_destination = os.path.expanduser(destination)
        if not os.path.exists(expanded_destination):
            os.mkdir(expanded_destination)
        temp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        temp_config_path = self._config_provider.get_temp_config_file_for_ripper(temp_path)
        subprocess_args = [
            self._config_provider.get_ruby_ripper_path(),
            '--defaults',
            '--file',
            temp_config_path
        ]
        print 'This is a big line'
        print u'[rip] Running rubyripper with {0}'.format(subprocess_args)
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, "")
        for line in lines_iterator:
            if line:
                print u'[rip] {0}'.format(line.strip().decode('utf-8'))
        utils.copy_content_to_directory(temp_path, expanded_destination)
        shutil.rmtree(temp_path)
        os.remove(temp_config_path)

class Mp3Tagger(object):
    def add_tags(self, source, artist='', album_artist='', album='',
                 title='', year='', genre='', comment='',
                 track_number=0, track_total=0, disc_number=0, disc_total=0):
        if source:
            if not os.path.exists(source):
                raise TaggerError('The source {0} does not exist.'.format(source))
            if os.path.isdir(source):
                raise TaggerError('The source must not be a directory.')
        else:
            raise ValueError('A source must be set for tagging an mp3.')
        tag = self._get_tag(source)
        self._add_artist_frame(tag, artist)
        self._add_album_artist_frame(tag, album_artist)
        self._add_title_frame(tag, title)
        self._add_album_frame(tag, album)
        self._add_year_frame(tag, year)
        self._add_genre_frame(tag, genre)
        self._add_comment_frame(tag, comment)
        self._add_track_number_frame(tag, track_number, track_total)
        self._add_disc_number_frame(tag, disc_number, disc_total)
        tag.save()

    def _add_artist_frame(self, tag, artist):
        if artist:
            tag.add(TPE1(encoding=3, text=artist))

    def _add_album_artist_frame(self, tag, album_artist):
        if album_artist:
            tag.add(TPE2(encoding=3, text=album_artist))

    def _add_title_frame(self, tag, title):
        if title:
            tag.add(TIT2(encoding=3, text=title))

    def _add_album_frame(self, tag, album):
        if album:
            tag.add(TALB(encoding=3, text=album))

    def _add_year_frame(self, tag, year):
        if year:
            tag.add(TDRC(encoding=3, text=year))

    def _add_genre_frame(self, tag, genre):
        if genre:
            tag.add(TCON(encoding=3, text=genre))

    def _add_comment_frame(self, tag, comment):
        if comment:
            tag.add(COMM(encoding=3, lang='eng', desc='comm', text=comment))

    def _add_track_number_frame(self, tag, track_number, track_total):
        track_number_string = str(track_number)
        track_total_string = str(track_total)
        if track_number < 10:
            track_number_string = '0{0}'.format(track_number)
        if track_total < 10:
            track_total_string = '0{0}'.format(track_total)
        tag.add(TRCK(encoding=3, text='{0}/{1}'.format(track_number_string, track_total_string)))

    def _add_disc_number_frame(self, tag, disc_number, disc_total):
        disc_number_string = str(disc_number)
        disc_total_string = str(disc_total)
        if disc_number < 10:
          disc_number_string = '0{0}'.format(disc_number)
        if disc_total < 10:
            disc_total_string = '0{0}'.format(disc_total)
        tag.add(TPOS(encoding=3, text='{0}/{1}'.format(disc_number_string, disc_total_string)))

    def apply_artwork(self, source, destination):
        if not source:
            raise ValueError('A cover art source must be supplied.')
        if not destination:
            raise ValueError('A destination must be supplied to apply cover art to.')
        if not os.path.exists(source):
            raise TaggerError('The cover art source does not exist.')
        if not os.path.exists(destination):
            raise TaggerError('The cover art destination does not exist.')
        audio_type = os.path.splitext(destination)[1][1:]
        if audio_type != 'mp3':
            raise TaggerError('The destination must be an mp3.')
        artwork_type = os.path.splitext(source)[1][1:]
        if artwork_type == 'jpg' or artwork_type == 'jpeg':
            mime_type = 'image/jpeg'
        elif artwork_type == 'png':
            mime_type = 'image/png'
        tag = self._get_tag(destination)
        tag.add(APIC(encoding=3, mime=mime_type, type=3, desc=u'cover', data=open(source).read()))
        tag.save()

    def remove_tags(self, source):
        try:
            tag = ID3(source)
            tag.delete()
        except ID3NoHeaderError:
            pass # There already is no tag, in which case, do nothing.

    def _get_tag(self, source):
        """
        This exists to handle mp3s that have no tags. It's horrendous, but
        I couldn't see a way to do a conversion between the EasyID3 type and
        a normal ID3 type.

        The steps are:
            * Attempt to load ID3 tag
            * Exception is thrown
            * Get an EasyID3 tag (easy=True)
            * Add a blank tag
            * Add a placeholder artist
            * Save the file
            * Reload as an ID3 object

        If you try and save without the placeholder, it doesn't write any tags (which makes sense),
        hence the need for the placeholder.
        """
        try:
            tag = ID3(source)
            return tag
        except ID3NoHeaderError:
            tag = File(source, easy=True)
            tag.add_tags()
            tag['artist'] = 'placeholder'
            tag.save()
            tag = ID3(source)
            return tag

class FlacTagger(object):
    def apply_artwork(self, source, destination):
        if not source:
            raise ValueError('A cover art source must be supplied.')
        if not destination:
            raise ValueError('A destination must be supplied to apply cover art to.')
        image_info = self._get_image_info(source)
        picture = Picture()
        with open(source, 'rb') as image:
            picture.data = image.read()
        artwork_type = os.path.splitext(source)[1][1:]
        if artwork_type == 'jpg' or artwork_type == 'jpeg':
            mime_type = 'image/jpeg'
        elif artwork_type == 'png':
            mime_type = 'image/png'
        picture.type = PictureType.COVER_FRONT
        picture.mime = mime_type
        picture.width = image_info[0]
        picture.height = image_info[1]
        tag = FLAC(destination)
        tag.add_picture(picture)
        tag.save()

    def remove_tags(self, source):
        if not source:
            raise ValueError('A source must be supplied.')
        tag = FLAC(source)
        tag.delete()

    def _get_image_info(self, source):
        image = Image.open(source)
        width, height = image.size
        bits = self._get_bits(image)
        return (width, height, bits)

    def _get_bits(self, image):
        try:
            bits = image.bits
            return bits
        except AttributeError:
            return None

    def add_tags(self, source, artist='', album_artist='', album='',
                 title='', year='', genre='', comment='',
                 track_number=0, track_total=0, disc_number=0, disc_total=0):
        if source:
            if not os.path.exists(source):
                raise TaggerError('The source {0} does not exist.'.format(source))
            if os.path.isdir(source):
                raise TaggerError('The source must not be a directory.')
        else:
            raise ValueError('A source must be set for tagging a flac.')
        tag = FLAC(source)
        self._add_artist_frame(tag, artist)
        self._add_album_artist_frame(tag, album_artist)
        self._add_title_frame(tag, title)
        self._add_album_frame(tag, album)
        self._add_year_frame(tag, year)
        self._add_genre_frame(tag, genre)
        self._add_comment_frame(tag, comment)
        self._add_track_number_frame(tag, track_number, track_total)
        self._add_disc_number_frame(tag, disc_number, disc_total)
        tag.save()

    def _add_artist_frame(self, tag, artist):
        if artist:
            tag['ARTIST'] = artist

    def _add_album_artist_frame(self, tag, album_artist):
        if album_artist:
            tag['ALBUMARTIST'] = album_artist

    def _add_title_frame(self, tag, title):
        if title:
            tag['TITLE'] = title

    def _add_album_frame(self, tag, album):
        if album:
            tag['ALBUM'] = album

    def _add_year_frame(self, tag, year):
        if year:
            tag['DATE'] = year

    def _add_genre_frame(self, tag, genre):
        if genre:
            tag['GENRE'] = genre

    def _add_comment_frame(self, tag, comment):
        if comment:
            tag['DESCRIPTION'] = comment

    def _add_track_number_frame(self, tag, track_number, track_total):
        track_number_string = str(track_number)
        track_total_string = str(track_total)
        if track_number < 10:
            track_number_string = '0{0}'.format(track_number)
        if track_total < 10:
            track_total_string = '0{0}'.format(track_total)
        tag['TRACKNUMBER'] = '{0}/{1}'.format(track_number_string, track_total_string)

    def _add_disc_number_frame(self, tag, disc_number, disc_total):
        disc_number_string = str(disc_number)
        disc_total_string = str(disc_total)
        if disc_number < 10:
          disc_number_string = '0{0}'.format(disc_number)
        if disc_total < 10:
            disc_total_string = '0{0}'.format(disc_total)
        tag['DISCNUMBER'] = '{0}/{1}'.format(disc_number_string, disc_total_string)
