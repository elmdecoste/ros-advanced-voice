# ros-advanced-voice
First year research project for the Gates Dell Complex's Building Wide Intelligence Initiative

## Running the program:

### Updating microphone source:
The microphone source needs to be set within the launch file. To set it, run
```
$ pacmd list-sources
```
Use the output from this to find the desired microphone for the system you are running on

### Launching
A launch file has been provided to startup all the required dependencies. To start:
```
$ roslaunch ros_advanced_voice bringup.launch
```

## Program Outline:

### Speech API 
Responsible for the speech-to-text functionality of the application. Will integrate with cloud speech-to-text software to utilize existing datasets and functionality.

    ```
    Broadcast: {
        Node: "/autospeech/receive"
        Data: String
    }
    ```

### Command Processer
Primary function is to parse the commands and break them into their multi-step functions.

    ```
    Listen: { 
        Node: "/autospeech/receive"
        Function: Parse input and create logical ROS commands from the speech
        Receive: String
    }

    Broadcast: {
        Node: "/autospeech/run"
        Data: String
    }
    ```

### Scheduler
Abstraction of the command running logic to its own Node

NOTE: The scheduler will continually queue new commands that it receives from the processor

    ```
    Listen: {
        Node: "/autospeech/run"
        Function: Sequentially run the commands requested
        Receive: String
    }
    ```

## Example
https://youtu.be/poMabkYfZCw

## Papers

Collobert, Ronan, et al. "Natural language processing (almost) from scratch." Journal of Machine Learning Research 12.Aug (2011): 2493-2537.
(http://www.jmlr.org/papers/volume12/collobert11a/collobert11a.pdf)

Candace Kamm, Marilyn Walker, Lawrence Rabiner, The role of speech processing in human–computer intelligent communication, Speech Communication, Volume 23, Issue 4, December 1997, Pages 263-278, ISSN 0167-6393, http://doi.org/10.1016/S0167-6393(97)00059-9.
(http://www.sciencedirect.com/science/article/pii/S0167639397000599)

G. Saridis, "Intelligent robotic control," in IEEE Transactions on Automatic Control, vol. 28, no. 5, pp. 547-557, May 1983. doi: 10.1109/TAC.1983.1103278
(http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1103278&isnumber=24201)

Chelba, Ciprian, and Frederick Jelinek. "Structured language modeling." Computer Speech & Language 14.4 (2000): 283-332.
(http://www.sciencedirect.com/science/article/pii/S0885230800901475)
