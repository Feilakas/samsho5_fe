# samsho5_fe
Samurai Shodown 5 Special (Final Edition) conversion tool

This Python tool takes certain files from SNK's Samurai Shodown NeoGeo Collection and outputs the file samsho5fe.zip:

# Usage.
**These scripts use the information provided in the following guide by Author alhumbra (Richard Roe) and as such are a derivative of those instructions: https://milkchoco.info/archives/3705**

- The main script is the samsho5_fe.py and after a successful execution will create the samsho5fe.zip file that can be used with the Final Burn Neo emulator.

**The syntax is python samsho5_fe.py <Input_folder> <Output_folder>.**

- The script samsho5_fe-SC is an older iteration of the above and produces the exact same file, albeit much MUCH slower, on account of using a single process (the newer script leverages multiple processes).

**The syntax is the same as above**

- The remaining scripts are simply parts of the main script and only perform one of the four needed functions which output the intended files.

**These scripts do not require any arguments and will assume the needed files are in the same folder as the script. They will also output their intended files in said folder.**

# Preparation
The files these scripts need as input may be found in "bundleMain.mbundle" and "bundleSamuraiShodown5Special.mbundle" which reside in "Steam\steamapps\common\SAMURAI SHODOWN NEOGEO COLLECTION\Bundle". 

This tool may be seen as complementary to ValadAmoleo's "[sf30ac-extractor](https://github.com/ValadAmoleo/sf30ac-extractor)" set of tools which can extact the mbundle files needed by this tool and convert Samurai Shodown 1 through 4.

ALTERNATELY, the mbundle contents may also be extracted by using **Luigi Auriemma's QuickBMS** tool with the **sf30_mbundle.bms script**.
You can find both at mr. Auriemma's webpage: http://aluigi.altervista.org/quickbms.htm

**Pleae note that I am not affiliated with either ValadAmoleo or mr. Auriemma nor their work in any way, shape or form.**


The files these scripts look for as input are the following:
- samsh5sp.cslot1_audiocrypt.dec (found in bundleSamuraiShodown5Special.mbundle)
- samsh5sp.cslot1_fixed.dec (found in bundleSamuraiShodown5Special.mbundle)
- samsh5sp.cslot1_ymsnd.dec (found in bundleSamuraiShodown5Special.mbundle)
- samsho5_fe.cslot1_maincpu (found in bundleMain.mbundle)
- SamuraiShodown5_FE.sprites.swizzled (found in bundleMain.mbundle)

The scripts perform checks to make sure all files are present and correct and will warn the user of any issues.

# DISCLAIMER
**These scripts are intended to be used for educational purposes ONLY and are provided AS-IS.**

**I cannot and do not make any claims or promises of any kind, either stated or implied, regarding these scripts or the manner that they may function, intended or unintended, nor do I assume ANY responsibility or liability for anything that may happen as a result of using said scripts.**
