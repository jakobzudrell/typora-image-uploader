# Import Libraries
import os
import sys
import uuid
import tempfile
from PIL import Image
from ftplib import FTP

# Gets the given cli arguments, which in this case
# should be images passed from typora in the formal: "image-path1.jpg" "image-path2.png"
# IMPORTANT: The first argument is always the script name
images = sys.argv
uploadedImages = []

# Weblink to images directory
webspaceUrl = 'yourWebspaceUrl'

# The FTP host- and username
hostname = 'yourFtpHostname'
username = 'yourFtpUsername'

# Set the FTP host
ftp = FTP(hostname)

# Login FTP user
# WARNING: Probably not the most secure method
ftp.login(user=username, passwd='yourFtpPassword')

# Create a temp directory for storing optimized images
with tempfile.TemporaryDirectory() as dir:
	# Log it
	# print('Created temporary directory at "' + dir +'"')

	# Reduce and temporarily store images
	for i in range(1, len(images)):
		# Get a single image
		image = Image.open(images[i])
		image = image.convert('RGB')
		newFileName =  str(uuid.uuid4()) + ".jpg"
		tmpFilePath = os.path.join(dir, newFileName)

		# Log it
		#print('Optimizing "' + images[i] + '"')

		# Save it with optimized and reduced quality
		image.save(tmpFilePath, optimize = True, quality = 75)

		# Log it
		#print('Done optimizing! Uploading via FTP....')

		# Upload
		ftp.storbinary('STOR ' + newFileName, open(tmpFilePath, 'rb'))

		# Log it
		#print('Uploaded as "' + newFileName + '"')

		# Finally append the image to our uploadedImages array
		uploadedImages.append(webspaceUrl + newFileName)


# IMPORTANT:  Close the connection
ftp.quit()

# Script has finished
#print('All Done ✔')
print('Uploaded images:')

for image in uploadedImages:
	print(image)