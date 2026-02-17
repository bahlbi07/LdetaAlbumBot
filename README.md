# Ldeta Album Bot

This is a Telegram bot designed to manage access to exclusive content channels, functioning as a simple storefront. It guides users through a multi-lingual interface to purchase access to different "albums" (private Telegram channels).

## How It Works
// The bot facilitates the purchase of access to private Telegram channels, referred to as "albums," through a structured conversational flow.
The bot operates through a conversation-based flow:

1.  **Language Selection**: A new user is prompted to select their preferred language from a list (Tigrinya, Amharic, English, Oromo, Saho).
2.  **Main Menu**: The user is presented with a list of available albums to purchase.
3.  **Purchase Flow**:
    *   The user selects an album.
    *   The bot asks if the user is in a specific location (e.g., Ethiopia) to determine the payment method.
    *   Payment instructions are displayed, and the user is asked to send proof of payment (like a screenshot).
4.  **Admin Verification**:
    *   The payment proof is forwarded to a designated admin chat.
    *   The admin receives a message with "Approve" and "Reject" buttons.
5.  **Access Grant/Rejection**:
    *   If the admin **approves**, the bot generates a single-use invite link to the corresponding private channel and sends it to the user.
    *   If the admin **rejects**, the user is notified that the verification failed.
6.  **Feedback**: For certain albums, the bot can be configured to automatically follow up with the user after a few days to ask for feedback.

## Features

-   **Multi-Language Support**: All user-facing text is translated based on the initial language selection.
-   **Conversation-Based Interface**: Uses inline keyboards and a state machine (`ConversationHandler`) to create a smooth user experience.
-   **Admin Approval System**: A simple and effective way for an administrator to manage access without leaving Telegram.
-   **Secure Access**: Generates one-time invite links to prevent unauthorized sharing.
-   **Automated Feedback Collection**: Uses a job queue to schedule follow-up messages.

## Setup

1.  **Clone the repository.**
2.  **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the root directory with the following variables:
    ```
    TELEGRAM_TOKEN="YOUR_BOT_TOKEN"
    ADMIN_CHAT_ID="YOUR_ADMIN_TELEGRAM_ID"
    ALBUM_ART_FILE_ID="OPTIONAL_TELEGRAM_FILE_ID_FOR_POSTER"
    ```
4.  **Configure Channels**: Update the `CHANNEL_IDS` dictionary in `bot.py` with your own private channel IDs.
5.  **Run the bot**:
    ```sh
    python bot.py
    ```
