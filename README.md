# conky-note

Note script for conky

Written by m3ss0r3m

Version 2

Usage: 
   
   note [OPTION] [-i|--index= <index>] CONTENTS

OPTION:

   -h, --help

      display help and exit
      
   -a, --add <content> [index with -i option]

      adding content to current page
      
   -r, --remove [content]|[index with -i option]

      remove content of current page
      
   -c, --create [index with -i option]

      create new page
  
   -d, --delete [index with -i option]

      delete page
    
   -t, --turn [next|pre]|[index with -i option]

      turn page
  
         next: next page
    
         pre|previous: previous page
  
   -o, --open [editor]

      open notes file (default : gedit)
  
   --info

      show current page number
  
   index : line number (of current page) or page number, depend on used [OPTION]
      
      
INSTALL:

You need install conky and configure conkyrc first.

Then, adding command to your note config in conkyrc:

    execpi 1 cat <notes current page location>
    
Example (using conky-colors):


    ############
    # - Note - #
    ############
    # type "ct help" in terminal for info
    ${voffset 4}${font Liberation Sans:style=Bold:size=8}NOTE $stippled_hr${font}
    ${voffset 4}${execpi 1 cat ~/.conkycolors/notes/current | fold -w 38 | sed 's/\[ \]/\[     \]/' | sed 's/\[X\]/\[ X \]/' | sed 's/\] /\] ${color2}/' | sed 's/$/${color}/' | sed 's/ X /${color0}${font ConkyColors:size=11}p${font}${color}${voffset -5}/'}
    ##########
  

Finally, you need config note command:

    sudo chmod +x note
    sudo mv note /bin/

That's it! Now you can use note command

    note -h
    
Of course, you need run conky to see result

    conky -c <path to your conkyrc>
    
conky-colors is recommended, use it for easier life :)

