# MusicBank

<hr noshade="noshade">

## Standards
<ul>
The MusicBank project aside from developing tools to manage large digital collection the project defines standards for these collections. These standards are the basis of the tools that are used to establish and maintain a well ordered collection.

<li><b>Nomenclature</b><p>
This subsection describes how a MusicBank collection is named
<ul>
<li><b>Language:</b><br>
The MusicBank uses English. Sorry guys but English is the
language of computer science and other tech stuff. It's the 2nd or 3rd most used language, it is taught in all the universities in the world, and it's the only language I know. Since I'm writing this, English. Given that, all databases will store the data in unicode. <p>

<li><b>Recording Format:</b><br>
The prefered file format of a recording is
<a href="https://en.wikipedia.org/wiki/FLAC" target="_blank">FLAC</a>. Since the price of storage has dropped to the point of being less than $0.50 per gigabyte it is cost effitive to us FLAC. FLAC also has the advanatage, aside from being lossless, it uses the OGG internal structure to store meta-data.<p>

<li><b>Dates:</b><br>
In the format yyyy-mm-dd. That is a 2 digit number for the month and day. If this number is under 10 then it is prepended with a zero. The date components are separated by a single hyphen. Why a 4 dight year? The first sound recordings were producted around 1877 by Thomas Edison. The first Jazz recordings were made in 1917. Enrico Caruso made his first recording in 1903. A file named 
<p><i>E-Caruso-04-01-05.flac</i></p>

Would be very confusing. Is the date 1905 or 2005? To avoid confusion we use a 4 dight year. Example: <p><i>1999-01-11</i><p>

<li><b>Disc Names:</b><br>
Unless the artist has explicitly named the individual disc, i.e. Nine Inch Nails - Fragile, the disc directory will be named Disc-## where # is a single digit. If the disc count is less that 10 then the first diget is a 0. Example: <p><i>Disc-01</i><p>

<li><b>Names:</b><br>
Names are in <a href="https://en.wikipedia.org/wiki/Camel_case" target="_blank">Camel case</a> with a hyphen between the words. The exception is a song title. All Songs titles are prepended with a 2 digit number which represents its' place in the order of songs. The first is 01 not 00. Between the ordinal digits and the song name is a double hyphen. Examples below:<p> 

<i>The-Smiths</i><br>
<i>Fables-Of-The-Reconstruction</i><br>
<i>04--Disturbance-At-The-Heron-House.mp3</i><br>
</ul>

<li><a name="dir_struct"><b>Directory structure</b></a><p>
People tend to think of music in on of 3 ways.<p>

<ol>
<li>An album. Either an LP or a cassette or a CD, an album is a collection of songs in a distinct order.<p>

<li>A single. This is an individual song.<p>

<li>A concert. This is a live performance of a musician or group of musician at a certain place at a certain time. The concert has a beginning and an end during which a set of songs are performed in a specific order.<p>

</ol><p>
The up shot is that one can think of an album, a single and a concert has a set of one or more songs which have certain characteristics which bind them together. In the digital realm a song is a file. The format of the file describes how it is dealt with.<p>

This document describes a scheme used to organize a collection of files in a hieratical file system to represent an album or a concert.<p>

All music is stored in a hierarchy file system starting at a point know as MUSIC_ROOT. This environment variable defines the start of the music tree. From there it procedures as follows.<p>
</ul>

<pre>
    MUSIC_ROOT/Data
              /Rip  /AlphaStage
                    /Stage
              /bin
              /Alpha/0-9/(Artist)
                    /A
                    /B
                    /C
                     ....
                    /Z
              /Archive/0-9/(Artist)
                      /A            
                      /B            
                      /C            
                       ....              
                      /Z
              /Other/Classical
                    /Clips
                    /Comedy
                    /Compilations
                    /Covers
                    /List
                    /Mixes
                    /Sountracks
                    /Various


    <a href="appendix.php#artist">Artist</a>/<a href="appendix.php#live">Live-Recordings</a>/<a
            href="appendix.php#date">Date</a>/<a href="appendix.php#rec-type">Type</a>/<a href="appendix.php#cover">Cover</a>/<a href="appendix.php#image">Image file</a>
                                    /<a href="appendix.php#music_file">Music File</a>
                                    /<a href="appendix.php#md5">MD5.txt</a>
                                    /<a href="appendix.php#notes">Notes.txt</a>
      /<a href="appendix.php#album">Album</a>          /<a href="appendix.php#disc">Disk-##</a>/<a href="appendix.php#music_file">Music File</a>
      /               /<a href="appendix.php#cover">Cover</a>/<a href="appendix.php#image">Image file</a>
      /               /<a href="appendix.php#album_xml">Album.xml</a>
      /               /<a href="appendix.php#notes">Notes.txt</a>
      /               /<a href="MB_appendic.html#tabs">Tabs</a>/<a
            href="appendix.php#guitar">Guitar</a>/<a href="appendix.php#tab_file">Tab file</a>
      /               /    /<a href="appendix.php#bass">Bass</a>  /<a href="appendix.php#tab_file">Tab file</a>
      /
      /<A href="appendix.php#misc">Misc</a>           /<a href="appendix.php#music_file">Music File</a>
      /<a href="appendix.php#notes">Notes</a>
      /<a href="appendix.php#playlist">PlayLists</a>
      /<a href="appendix.php#md5">MD5.txt</a>

        </pre>
</pre>

## Definations
<p>
    </ul>
<hr noshade="noshade">

<div style="font-size: 12pt">
<ul>

<!-- AAC -->
<li>
<a style="font-weight: bold;" name="aac">AAC</a><br>
Advanced Audion Coding (AAC) is a lossy data compression scheme for digital music files. It was designed to compete with MP3 in terms of audio quality. AAC is used the 
<a href="http://www.apple.com/ipod/ipod.html" target="_blank">Apple iPod.</a> 
Other portable music players also support AAC. The tool, 
<a href="appendix.php#faac">FAAC</a> is used to convert
<a href="appendix.php#wav">WAV</a> file to AAC. See the 
<a href="http://en.wikipedia.org/wiki/Advanced_audio_coding" target="_blank">AAC</a> 
entry on 
<a href="http://en.wikipedia.org/wiki/Main_Page" target="_blank">Wikipedia</a> 
for more information on MP3.
</li><p>

<!-- Album -->
<li>
<a name="album"><b>Album</b></a><br>
An Album is a finite collection of songs organized in a specific order. </li><p>

<!-- Album.json -->
<li>
<a style="font-weight: bold;" name="album_json">Album.json</a><br>
</li><p>

<!-- Alpha -->
<li>
<a style="font-weight: bold;" name="alpha">Alpha</a><br>
</li>

<!-- AlphaStage -->
<li>
<a style="font-weight: bold;" name="AlphaStage">AlphaStage</a><br>
</li>

<!-- Artist -->
<li>
<a name="artist"><b>Artist</b></a><br>
The artist name, either his/her proper name such as Bob Dylan, the Group name such as The-Band. The name is in Camel Case.
</li><p>

<!-- Bass -->
<li>
<a style="font-weight: bold;" name="bass">Bass</a><br>
See the 
<a href="http://en.wikipedia.org/wiki/Bass_guitar" target="_blank">
Bass Guitar</a> 
entry on <a href="http://en.wikipedia.org/wiki/Main_Page" target="_blank">Wikipedia</a> 
for more information on bass guitars.
</li><p>

<!-- Bin -->
<li>
<a style="font-weight: bold;" name="bin">Bin</a><br>
</li>

<!-- Camel Case -->
<li>
<a style="font-weight: bold;" name="camel_case">Camel Case</a><br>
See the <a href="http://en.wikipedia.org/wiki/Camel_case" target="_blank">Camel Case</a> entry on <a href="http://en.wikipedia.org/wiki/Main_Page" target="_blank">Wikipedia</a> for more information on camel case.
</li><p>

<!-- Classical -->
<li>
<a style="font-weight: bold;" name="classical">Classical</a><br>
</li>

<!-- Clips -->
<li>
<a style="font-weight: bold;" name="clips">Clips</a><br>
</li>

<!-- Comedy -->
<li>
<a style="font-weight: bold;" name="comedy">Comedy</a><br>
</li>

<!-- Compilations -->
<li>
<a style="font-weight: bold;" name="comp">Compilations</a><br>
</li>

<!-- Cover -->
<li>
<a style="font-weight: bold;" name="cover">Cover</a><br>
This directory contains the cover art of the album in some electronic format (gif, jpg, png, etc.)
</li><p>

<!-- Covers -->
<li>
<a style="font-weight: bold;" name="covers">Covers</a><br>
</li>

<!-- Data -->
<li>
<a style="font-weight: bold;" name="data">Data</a><br>
</li>

<!-- Date -->
<li>
<a style="font-weight: bold;" name="date">Date</a><br>
</li>

<!-- Disk # -->
<li>
<a name="disc"><b>Disk #</b></a><br>
A serial number of the discs of the album in question. Most albums only have one disc but when the album has more than one disc they are numbered in sequence. The artist may chose to label the discs something other than "Disc 1", "Disc 2", etc. The album "Fragile" by "Nine Inch Nails" is an example. Those 2 discs were labeled "Left" and "Right".
</li><p>

<!-- FAAC -->
<li>
<a style="font-weight: bold;" name="faac">FAAC</a><br>
</li>

<!-- FLAC -->      
<li>
<a style="font-weight: bold;" name="flac">FLAC</a><br>
See the <a href="http://en.wikipedia.org/wiki/Flac" target="_blank">FLAC</a> entry on <a
    href="http://en.wikipedia.org/wiki/Main_Page"
    target="_blank">Wikipedia</a> for more information on FLAC.
</li><p>

<!-- Guitar -->
<li>
<a style="font-weight: bold;" name="guitar">Guitar</a><br>
See the <a href="http://en.wikipedia.org/wiki/Guitar" target="_blank">Guitar</a> entry on <a
    href="http://en.wikipedia.org/wiki/Main_Page"
    target="_blank">Wikipedia</a> for more information on guitars. 
</li><p>

<!-- Image File -->
<li>
<a style="font-weight: bold;" name="image">Image file</a><br>
This is the cover art of the album in some electronic format (gif, jpg, png, etc.)
</li><p>

<!-- Lists -->
<li>
<a style="font-weight: bold;" name="lists">Lists</a><br>
</li>

<!-- Live Recordings -->
<li>
<a style="font-weight: bold;" name="live">Live Recordings</a><br>
</li>

<!-- MD5 -->
<li>
<a name="md5"><b>MD5</b></a><br>
An MD5, and a related SHA1, is a unique digital fingerprint of that individual file. See the <a href="http://en.wikipedia.org/wiki/Md5"
    target="_blank">MD5</a> entry on <a
    href="http://en.wikipedia.org/wiki/Main_Page"
    target="_blank">Wikipedia</a> for more information on MD5 and
  SHA1. In this instance, each music file has an MD5. This is to
</li><p>

<!-- MP3 -->
<li>
<a style="font-weight: bold;" name="mp3">MP3</a><br>
  See the <a href="http://en.wikipedia.org/wiki/Mp3"
    target="_blank">MP3</a> entry on <a
    href="http://en.wikipedia.org/wiki/Main_Page"
    target="_blank">Wikipedia</a> for more information on MP3.
</li><p>

<!-- MUSIC_ROOT -->
<li>
<a style="font-weight: bold;" name="music_root">MUSIC_ROOT</a><br>
</li>

<!-- Misc -->
<li>
<a style="font-weight: bold;" name="misc">Misc</a><br>
</li>

<!-- Mixes -->
<li>
<a style="font-weight: bold;" name="mixes">Mixes</a><br>
</li>

<!-- Music File -->
<li>
<a style="font-weight: bold;" name="music_file">Music file</a><br>
</li>

<!-- Notes -->
<li>
<a style="font-weight: bold;" name="notes">Notes</a><br>
</li>

<!-- Ogg -->
<li>
<a style="font-weight: bold;" name="ogg">Ogg</a><br>
  See the <a href="http://en.wikipedia.org/wiki/Ogg">Ogg</a> entry on
  <a href="http://en.wikipedia.org/wiki/Main_Page">Wikipedia</a> for
  more information on ogg.
</li><p>

<!-- Other -->
<li>
<a style="font-weight: bold;" name="other">Other</a><br>
</li>

<!-- PCM -->
<li>
<a style="font-weight: bold;" name="pcm">PCM</a><br>
  See the <a href="http://en.wikipedia.org/wiki/PCM">PCM</a> entry on
  <a href="http://en.wikipedia.org/wiki/Main_Page">Wikipedia</a> for
  more information on PCM. 
</li><p>

<!-- Play Lists -->
<li>
<a style="font-weight: bold;" name="playlist">Play Lists</a><br>
</li>

<!-- Recording Type -->
<li>
<a style="font-weight: bold;" name="rec-type">Recording Type</a?<br>
</li><p>

<!-- Rip -->
<li>
<a style="font-weight: bold;" name="rip">Rip</a><br>
</li>

<!-- Shorten -->
<li>
<a style="font-weight: bold;" name="shorten">Shorten</a><br>
  See the <a href="http://en.wikipedia.org/wiki/Shorten">Shorten</a>
  entry on <a
    href="http://en.wikipedia.org/wiki/Main_Page">Wikipedia</a> for 
  more information on Shorten.
</li><p>

<!-- Soundtrack -->
<li>
<a style="font-weight: bold;" name="soundtrack">Soundtrack</a><br>
</li>

<!-- Stage -->
<li>
<a style="font-weight: bold;" name="stage">Stage</a><br>
</li>

<!-- Tab file -->
<li>
<a style="font-weight: bold;" name="tab_file">Tab file</a><br>
</li>

<!-- Tabs -->
<li>
<a style="font-weight: bold;" name="tabs">Tabs</a><br> This
directory contains tablature, either guitar or bass, of the songs
contained in this album. See the <a target="_blank"
href="http://en.wikipedia.org/wiki/Tablature">Tablature</a> entry on
<a target="_blank"
href="http://en.wikipedia.org/wiki/Main_Page">Wikipedia</a> for more
information. 
</li><p>

<!-- Various -->
<li>
<a style="font-weight: bold;" name="varios">Various</a><br>
</li>

<!-- WAV -->
<li>
<a style="font-weight: bold;" name="wav">WAV</a><br>
  See the <a target="_blank"
    href="http://en.wikipedia.org/wiki/Wav">WAV</a> entry on
  <a target="_blank"
    href="http://en.wikipedia.org/wiki/Main_Page">Wikipedia</a> for more
  information.
</li><p>
</ul>
</div>