Quick History Selection UI for Maya (ver 0.5)
===
Scripting Language: PYTHON

Development Environment: Maya 2011 x64

Author: Andrew Glisinski

First Release: Feb 5 2016

Updates:

*   February 5 2016 - Initial Release (0.1)
*   February 6 2016 - Cycles Feature (0.2)
*   February 7 2016 - Set Functions (0.3)
*                   - Organization (0.4)
*   February 8 2016 - Sort by Type (0.45)
*   March 3 2016    - Feature Add: (0.5)
                    - Add/Remove to Sets
                    - Dockable
                    - Find/Replace
                    - Export/Import to JSON file
                    - Modify:
                    - adding to a set now adds a sorted(list)

-------------------
*   Q: What does this do?
    Quick History Selection opens up a window that can temporarily hold selection sets (not the built-in Maya sets) that you can easily toggle between.
*   Q: Why not just use regular quick selection sets?

    Primarily because sometimes you just want to save a selection of something (ie. vertices) for a short period of time. Saving out as sets seems a little unnecessary, and this is just a quick and dirty approach with some key features that relay a little more information at glance than selection sets.
*   Q: What versions of Maya support this?

    Hopefully all of them? I developed this and tested it in Maya 2011. I don't provide any sort of assistance or guarantees with this script beyond claiming it will work. Don't use it in a commercial environment until it's fully tested to do what you expect. No modifications to the scene are made unless it's the 'globalSelectionDictionary' dictionary object that we instantiate before running the script.

-------------------
Further Notes:

- 'globalSelectionDictionary' is a dictionary being instantiated in Maya's local space, it should stick around between closing/opening the UI window. Since this is not saved in any way after the program exits, all that data will be lost. Maybe in the future I'll add an option for JSON or something.
- Don't re-instantiate the dictionary unless you wish for all your selection data to be deleted! 
- See the install guide for info on how to save out a shelf icon
