# conky-note
Note script for conky

Written by m3ss0r3m

Usage: note [OPTION] [-i, --index] <line number> CONTENTS

OPTION:

-h, --help

  display help and exit
      
-a, --add

  adding content to task file
      
-r, --remove

  remove content to task file
      
-b, --blank

  remove all contents in task file
      
-o, --open [editor]

  open notes file (default : gedit)
      
INSTALL:

You need install conky and configure conkyrc first.

Then, adding command to your note config in conkyrc:

    execpi 1 cat <notes directory>
    
Example (using conky-colors):


    ############
  
    # - Note - #
  
    ############
  
    # type "ct help" in terminal for info
  
    ${voffset 4}${font Liberation Sans:style=Bold:size=8}NOTE $stippled_hr${font}
  
    ${voffset 4}${execpi 1 cat ~/.conkycolors/notes | fold -w 38 | sed 's/\[ \]/\[     \]/' | sed 's/\[X\]/\[ X \]/' | sed 's/\] /\] ${color2}/' | sed 's/$/${color}/' | sed 's/ X /${color0}${font ConkyColors:size=11}p${font}${color}${voffset -5}/'}
  
    ##########
  

Finally, you need config note command:

    sudo chmod +x note
    sudo mv note /bin/

That's it! Now you can use note command

    note -h
    
Of course, you need run conky to see result

    conky -c <path to your conkyrc>
    
conky-colors is recommended, use it for easier life :)

