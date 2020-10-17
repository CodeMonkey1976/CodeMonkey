# Artifact One Narrative: Software Design and Engineering

##### The first artifact is from my final project in CS 410: Reverse Software engineering. I wrote the C version of this program in June of 2020, and it was reversed engineered from a compiled legacy executable. The program allows a user to login and makes change student grades.  The program is riddled with design flaws, but it works exactly like the legacy program it was reversed engineered from.

##### I chose this artifact because even though the original program worked as intended, I do not believe that it worked as it should. When I first wrote this program, I had a list of things that I wanted to change, but could not because that was not the assignment. The original assignment asked to write the legacy program in C, and that is what I did. I made several artifact improvements. 

##### One of the things that I wanted to showcase was my attention to detail. I rewrote the program in Python, and addressed some of the items from my “list.” One thing that made my list was the names and the grades did not align. This kind of detail is important to me. I also did not like how the user was forced to edit every student on the list to make a change. I added a menu to allow the user to edit one student at a time. The user can also change the student’s name as well as the grade. The changes are then saved to a file. The file will be reloaded on the program restart. Programs handling sensitive data such as this needs better security. I hashed the password with an MD5 hash. According to (Mehrabani & Eshghi, 2012) “It gets a string with an arbitrary length as input and produces a message with 128-bit length called message-digest or fingerprint as output.” Currently, the program only has two users. Gregg with a password of “123”, and “Rusty” with a password of “456”. 

##### I enjoy writing code. I find that the C languages are a bit of a challenge for me. I learned a significant amount in this project. I learned how to read and write data to and from files. I was able to use this data to make decisions. I also learned how to apply a hash to a string for better security. This artifact was enhanced by rewriting it in Python, making the menus more efficient, enhanced the security of the program, and gave the program the ability to save changes made.

##### References
###### Mehrabani, Y. S., & Eshghi, M. (2012). Design of an ASIP processor for MD5 hash algorithm. 2012 20th Telecommunications Forum (TELFOR) Telecommunications Forum (TELFOR) (pp. 548-541). Belgrade: IEEE.

