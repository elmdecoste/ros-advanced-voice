# ros-advanced-voice
First year research project for the Gates Dell Complex's Building Wide Intelligence Initiative

## Program Outline:

### Speech API 

   * Responsible for the speech-to-text functionality of the application. Will integrate with
    cloud speech-to-text software to utilize existing datasets and functionality. *

    ```
    Broadcast: {
        Node: "/autospeech/receive"
        Data: String
    }
    ```

### Command Processer

    * Primary function is to parse the commands and break them into their multi-step functions *

    ```
    Listen: { 
        Node: "/autospeech/receive"
        Function: Parse input and create logical ROS commands from the speech
        Receive: String
    }

    Listen: {
        Node: "/autospeech/status"
        Function: Check if the scheduler is currently executing
        Receive: Boolean
    }

    Broadcast: {
        Node: "/autospeech/run"
        Data: JSON
    }
    ```

### Scheduler
    
        * Abstraction of the command running logic to its own Node

        NOTE: If the scheduler recieves a new instruction set, it will stop the previous
        instructions and continue with the newly received ones. *

    ```
    Listen: {
        Node: "/autospeech/run"
        Function: Sequentially run the commands requested
        Receive: JSON
    }

    Broadcast: {
        Node: "/autospeech/status"
        Data: Boolean
    }
    ```

## Papers

Collobert, Ronan, et al. "Natural language processing (almost) from scratch." Journal of Machine Learning Research 12.Aug (2011): 2493-2537.
http://www.jmlr.org/papers/volume12/collobert11a/collobert11a.pdf

Candace Kamm, Marilyn Walker, Lawrence Rabiner, The role of speech processing in human–computer intelligent communication, Speech Communication, Volume 23, Issue 4, December 1997, Pages 263-278, ISSN 0167-6393, http://doi.org/10.1016/S0167-6393(97)00059-9.
(http://www.sciencedirect.com/science/article/pii/S0167639397000599)
