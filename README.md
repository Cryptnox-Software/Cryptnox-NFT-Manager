# Cryptnox-NFT-Manager

### Overview
A Graphical User Interface (GUI) to load NFT assets onto Cryptnox NFT cards.

### Usage
(1) Select one of 3 options to input asset information.<br>
(2) Provide URL/File <and/or> fill in form<br>
(3) Execute load<br>

### Input methods
* URL<br>
  Inputting the asset URL and clicking "Get fields" automatically fills corresponding fields with information of the asset retrieved from the web utilizing the given URL.<br>
* File <br>
  Selecting a file with NFT information automatically fills corresponding fields with data from the selected file.
* Manual <br>
  This option allows users to freely input NFT data in all fields.

### Background
The application presumes a non-initialized card. If initialized, card be reset using the "reset" command in the [Cryptnoxpro CLI](https://github.com/Cryptnox-Software/cryptnoxpro).
After data has been sucessfully written to card, a dialog box appears to inform the user of the successful operation, exiting the application afterwards.
The card is then initialized with the data and can be viewed in the [Cryptnox Gallery](https://github.com/Cryptnox-Software/Cryptnox-Gallery).
