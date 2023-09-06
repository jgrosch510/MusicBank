# MusicBank
## Standards

<ul>
  <li><b>Nomenclature</b><p>
  This subsection describes how a MusicBank collection is named
  <ul>
    <li><b>Language:</b><br>
    The MusicBank uses English. Sorry guys but English is the
    language of computer science and other tech stuff. It's the most used language, it is taught in all the universities in the world, and it's the only language I know. Since I'm writing this, English. Given that, all databases will store the data in unicode. <p>

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

  <li><a name="dir_struct"><b>Directory structure</b></a><p> People tend to think of music in on of 3 ways.<p>

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


    <a href="appendix.md#artist">Artist</a>/<a href="appendix.md#live">Live-Recordings</a>/<a
            href="appendix.md#date">Date</a>/<a href="appendix.md#rec-type">Type</a>/<a href="appendix.md#cover">Cover</a>/<a href="appendix.md#image">Image file</a>
                                    /<a href="appendix.md#music_file">Music File</a>
                                    /<a href="appendix.md#md5">MD5.txt</a>
                                    /<a href="appendix.md#notes">Notes.txt</a>
          /<a href="appendix.md#album">Album</a>          /<a href="appendix.md#disc">Disk-##</a>/<a href="appendix.md#music_file">Music File</a>
          /               /<a href="appendix.md#cover">Cover</a>/<a href="appendix.md#image">Image file</a>
          /               /<a href="appendix.md#album_xml">Album.xml</a>
          /               /<a href="appendix.md#notes">Notes.txt</a>
          /               /<a href="MB_appendic.md#tabs">Tabs</a>/<a
            href="appendix.md#guitar">Guitar</a>/<a href="appendix.md#tab_file">Tab file</a>
          /               /    /<a href="appendix.md#bass">Bass</a>  /<a href="appendix.md#tab_file">Tab file</a>
          /
          /<a href="appendix.md#misc">Misc</a>           /<a href="appendix.md#music_file">Music File</a>
          /<a href="appendix.md#notes">Notes</a>
          /<a href="appendix.md#playlist">PlayLists</a>
          /<a href="appendix.md#md5">MD5.txt</a>
        </pre>
