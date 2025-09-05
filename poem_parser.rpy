# As this was originally written with DDLC poems in mind, you will see some DDLC stuff in here, it's made for modding that game.
# If you want to use this for your own game, you can remove the DDLC stuff and it should work fine.  Besides the Poem class that DDLC uses as that is not provided here.
# If you want to use this for different classes, you can by changing around and adding onto the special character formatting.

init python:
    def parse_poem(file):
        """
        hparses a text files in a `poems` folder in the game directory and creates a `Poem` instance
        first letter of the filename is used as author:
            s: sayori
            m: monika
            n: natsuki
            y: yuri
            p: mc
            anything else or no letter: generic
        filename will be loaded into the dictionary as a key without the extension.
        first lines of the file can start with special characters to set properties (these will pass the defaults if not used):
            `# `: title
            `@ `: style 
            `% `: paper, if image path is followed by braces, will be passed to `Transform()` with the arguments inside the paratheses
            `& `: music
            `! `: separate title from text
            `{properties}`: properties
        rest of the file is used as text

        start with a blank line to separate properties from text
        """
        with open(f"{renpy.config.gamedir}/{file}", encoding="utf-8") as f:
                    lines = f.readlines()
                    author = author_generic # if you don't have this default, change it None before your game breaks
                    title = ""
                    style = True
                    paper = None
                    music = None
                    separate_title_from_text = False
                    filename = file[file.rfind("/") + 1:file.rfind(".")]
                    properties = {}

                    # This is for poem author, MC is here because this was made for a mod that actually has MC write poems
                    # change out the default variables if you don't have them defined before your game breaks
                    if filename.startswith("s"):
                        author = author_s
                    elif filename.startswith("m"):
                        author = author_m
                    elif filename.startswith("n"):
                        author = author_n
                    elif filename.startswith("y"):
                        author = author_y
                    elif filename.startswith("p"):
                        author = author_mc
                    
                    # below is used for special character formatting for special properties, change out or add on to these for other classes.  What's there now is for DDLC's Poem class.
                    while True:
                        line = lines[0].strip()
                        if not line:
                            break
                        
                        if line.startswith("# "):
                            title = line[2:].strip()
                            del lines[0]
                            continue
                        
                        if line.startswith("@ "):
                            style = line[2:].strip() or True
                            if style.lower() in ("false", "0", "no"):
                                style = False
                            elif style.lower() in ("true", "1", "yes"):
                                style = True
                            del lines[0]
                            continue
                        
                        if line.startswith("% "):
                            paper = line[2:].strip() or None
                            if "{" in paper and paper.endswith("}"): # this is parsed assuming the image path doesn't contain any braces
                                args = eval(paper[paper.find("{"):])
                                if not isinstance(args, dict):
                                    raise ValueError(f"Invalid Transform arguments in poem file '{file}'")
                                paper = Transform(paper[:paper.find("{")].strip(), **args)
                            else:
                                paper = renpy.easy.displayable(paper) or None
                            del lines[0]
                            continue
                        
                        if line.startswith("& "):
                            music = line[2:].strip() or None
                            if music.lower() in ("false", "0", "no"):
                                music = False
                            elif music.lower() in ("true", "1", "yes"):
                                music = True
                            del lines[0]
                            continue
                        
                        if line.startswith("! "):
                            separate_title_from_text = line[2:].strip().lower() in ("true", "1", "yes")
                            del lines[0]
                            continue

                        if line.startswith("{"):
                            properties = eval(line.strip())
                            if not isinstance(properties, dict):
                                raise ValueError(f"Invalid properties in poem file '{file}'")
                            del lines[0]
                            continue
                    return Poem(author, "".join(lines).strip(), title=title, style=style, paper=paper, separate_title_from_text=separate_title_from_text, music=music, **properties) # or whatever class your using

# if you want to show this in your DDLC mod, add this if block to your show_poem function/label (Uncommented, it's commented out so it won't break your game if you just throw the file in there)
# if isinstance(poem, str):
#     if preferences.language is None:
#         filepath = f"poems/{poem}.txt"
#     else:
#         filepath = f"tl/{preferences.language}/poems/{poem}.txt"
#     if filepath:
#         poem = parse_poem(filepath)

# all default language poems are located in game/poems/ and all translated poems are located in game/tl/{language}/poems/
# poem writing instructions can be found in the `example poem.txt` file bundled with this script.