PATH = "/Volumes/TOSHIBA EXT/SYTOX-NikonTI-2/";
input_folder = "1/";
new_folder_add = "1/additive/";

files = getFileList(PATH + input_folder);
print(files.length+" images in the directory " + PATH);

if (!File.exists(PATH + new_folder_add)){
  	File.makeDirectory(PATH + new_folder_add);
  	if (!File.exists(PATH + new_folder_add)){
  		exit("Unable to create a directory for masks. Check User permissions.");
  	}
  }
// Process each image with the trained model and save the results.
for (i=0; i<files.length; i++) {
	// avoid any subfolder
	if (endsWith(files[i], ".tif")){
		
		// store the name of the image to save the results
		image_name = File.getNameWithoutExtension(PATH + input_folder + files[i]);

		// open the image
		open(PATH + input_folder + files[i]);
		
name = getTitle();
getDimensions(width, height, channels, slices, frames);

//frame 0 as the initial reference image
selectWindow(name);
run("Duplicate...", "duplicate range=1-1");
rename("ref");

//loop each frame from 1 to the next
for (t = 1; t < frames; t++) {
    //current frame
    selectWindow(name);
    run("Duplicate...", "duplicate range=" + t + "-" + t);
    rename("next");
    
    //ImageCalculator OR operation between ref and next
    imageCalculator("OR create", "ref","next");
    selectWindow("next");
    close();
    selectWindow("ref");
    close();  
    
    //save result with frame number
    saveAs("Tiff", PATH + new_folder_add+image_name + "_" + t + ".tif");
    rename("ref");
    
}

//close the final reference image
selectWindow("ref");
close();