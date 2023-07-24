#Building a Media Sharing Website

Create a bucket named "assignmentarchitecture" using either CLI or the AWS UI. For this assignment, the UI is recommended due to frequent changes.
Choose a unique name for the bucket that has not been used before.
Select the region where the bucket should be created and press the "Create" button.
After creating the bucket, add your media files to it.
By default, the bucket is not accessible to the public. To make it public, go to the "Permissions" section under "Block public access (bucket settings)."
Assign a policy to the bucket to allow outside users to perform actions like PUT and GET. Use the policy generator and specify the required permissions, such as "PutObject" and "GetObject."
Creating an Amazon DynamoDB Database

Click the "Create Table" button on the DynamoDB console in your AWS account.
Specify a name, primary key, and any additional properties for your table. For example, use "assignment" as the table name with "ID" as the primary key.
Set up your table's throughput and encryption preferences according to your requirements.
Review your table's specifics and create the table.
Launching a new Amazon EC2 Instance

In the EC2 console of your AWS account, click on the "Launch Instance" button.
Choose an Amazon Machine Image (AMI) for your instance (e.g., the default option).
Select an instance type based on your application requirements. A "t2.micro" instance should suffice for basic work.
Configure your instance details, including network settings, storage, and security groups.
Make sure to attach the "LabRole" under Additional settings. This allows using IAM policies assigned to the "LabRole" role without needing access keys or credentials.
Review your instance details and launch your instance.
Creating the Web Application using Python inside EC2

Access the CLI of the instance or connect via SSH. Install Python, Pip, Pillow, Boto3, and Flask.
Python is used to write the main code (app.py in our case) and index.html to display the webpage.
Pip is a package manager for Python, used to install other libraries and modules.
Boto3 is an AWS SDK for Python, allowing interaction with services like S3 and EC2.
Pillow is a Python library used for web development and ML, including resizing and converting image formats.
Flask is a web framework for Python that helps build web applications. It receives images, creates thumbnails, and displays them on the webpage table. It also sends metadata to DynamoDB.
How Everything Works

index.html: This file lays out the forms where users can input their information. It displays the information in a table with an option to delete each entry received.
app.py: This file defines the Flask application, routes URLs to functions handling requests, returns HTML content to the browser, connects with the database and S3, and displays content on the browser.
Both S3 and DynamoDB are connected via EC2, which can send data and delete resources simultaneously.
By following these steps, you can build a media sharing website that securely stores user data, media files, and metadata in AWS services like S3 and DynamoDB.
