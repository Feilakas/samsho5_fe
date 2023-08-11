# samsho5_fe
Samurai Shodown 5 Special (Final Edition) conversion tool

This is a set of Python scripts which take certain files from SNK's Samurai Shodown NeoGeo Collection and output the file samsho5fe.zip:
/**These scripts use the information provided in the followin URL link by Author alhumbra (Richard Roe) and as such are a derivative of those instructions: https://milkchoco.info/archives/3705**

- The main script is the samsho5_fe.py and after a successful execution will create the samsho5fe.zip file that can be used with the Final Burn Neo emulator.

**The syntax is python samsho5_fe.py <Input_folder> <Output_folder>.**

- The script samsho5_fe-SC is an older iteration of the above and produces the exact same file, albeit much MUCH slower, on account of using a single process (the above script leverages multiple processes).

**The syntax is the same as above**

- The remaining scripts are simply parts of the main script and only perform one of the four needed functions which output the intended files.

**These scripts do not require any syntax and will assume the needed files are in the same folder as the script. The will also output their intended files in said folder.**


The files these scripts need as input may be found in "bundleSamuraiShodown5Special.mbundle" which resides in "Steam\steamapps\common\SAMURAI SHODOWN NEOGEO COLLECTION\Bundle".
The mbundle contents may be extracted by using **Luigi Auriemma's QuickBMS** tool with the **sf30_mbundle.bms script**.

You can find both at mr. Auriemma's webpage: http://aluigi.altervista.org/quickbms.htm

**I am not affiliated with mr. Auriemma nor his work in any way, shape or form.**


The files these scripts look for as input are the following:
- samsh5sp.cslot1_audiocrypt.dec
- samsh5sp.cslot1_fixed.dec
- samsh5sp.cslot1_ymsnd.dec
- samsho5_fe.cslot1_maincpu
- SamuraiShodown5_FE.sprites.swizzled

The scripts perform checks to make sure all files are present and correct and will warn the user of any issues.


**These scripts are intended to be used for educational purposes ONLY and are provided AS-IS.**

**I cannot and do not make any claims or promises on whether they will function as you intend them to nor do I assume ANY responsibility for anything that may happen as a result of using said scripts.**
