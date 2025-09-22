# Description: This ticket requires the developer to update the existing feature to show the already generated images.

**Detail**: In the current implementation, when the user press the arrow button, the application shows a generated image. There is button called modify, which takes in the same image with an additional prompt, and makes the api call. The final result is again displayed on the screen, but there is no way to see what was the previous response, which image was attached with the prompt last time. Hence, the client has requested an update in this feature.

**Implementaion Plan**: The high level implementaion plan is to create a pane, on the left side of the home screen where the generated images will be shown. Initially, this pane will not be visible, once an image is created, this will be shown with one image, in second iteration, you should see 2 images and so on.
Please see the design image to get a better understanding of the desing. 
**REFERENCE IMAGE OF DESIGN : tickets\backbtnimg.png**

**Additional requirments**: 
1- Make sure the image pane is not visible in the start.
2- Number of images shown shold dymanically adjust. 
3- In case there are more than 4 images, it should show a scroller to move up and down so that the size do not grow more than the given screen size (Bad design).
4- The pane should show the images previow and not only the links.