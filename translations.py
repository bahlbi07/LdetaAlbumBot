# translations.py

TRANSLATIONS = {
    'en': {
        'welcome': "Welcome <b>{user_name}</b>!\n\nPlease choose your language:",
        'main_menu': "Welcome to the official sales bot for <b>'Lideta Mariam Choir Vol. 4'</b> album.",
        'buy_album_button': "🛒 Purchase Album",
        'about_album_button': "ℹ️ About This Album",
        'back_button': "🔙 Back to Main Menu",
        'payment_instructions': (
            "Great! The price of the album is <b>{album_price} ETB</b>.\n\n"
            "Please use one of the following payment methods:\n\n"
            "<b><u>1. Commercial Bank of Ethiopia (CBE):</u></b>\n"
            "<b>Name:</b> Mahber Mezamran Lideta Maryam K.MK\n"
            "<b>Account No:</b> 1000639550323\n\n"
            "<b><u>2. Bank of Abyssinia (BOA):</u></b>\n"
            "<b>Name:</b> Mahber Mezamran Lideta Maryam\n"
            "<b>Account No:</b> 196302506\n\n"
            "⚠️ <b>Important:</b> After paying, please send the receipt (screenshot) to our admin at @Dmtsibereket. "
            "You will receive your invite link shortly after verification."
        ),
        'about_album_text': (
            "<b><u>About the 4th Album</u></b>\n\n"
            "This is the fourth album prepared by the 'Lideta Mariam Choir Qumsna Mekelle', "
            "containing many new and spiritual hymns.\n\n"
            "<i>(Additional information or tracklist can be added here.)</i>"
        ),
        'saho_unavailable': "The Saho (Irob) language section is currently under construction. Please select another language for now.",
        'payment_received_admin': "New payment slip received from user {user_mention} (ID: `{user_id}`). Please verify.",
        'approve_usage': "Usage: /approve <user_id>\nExample: /approve 123456789",
        'approval_success_admin': "✅ Success! Invite link has been sent to user {user_id}.",
        'approval_not_admin': "❌ Sorry, this command can only be used by the designated admin.",
        'payment_success_user': (
            "✅ <b>Your payment has been successfully verified!</b> ✅\n\n"
            "Thank you so much for your support.\n\n"
            "You can now join the private channel using this one-time invite link:\n"
            "<b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ We are sorry, but there was an issue verifying your payment slip. Please contact @Dmtsibereket for assistance.",
        'rejection_success_admin': "User {user_id} has been notified about the payment rejection.",
    },
    'ti': {
        'welcome': "እንኳዕ ብደሓን መጻእካ <b>{user_name}</b>!\n\nበጃኻ ቋንቋ ምረጽ፦",
        'main_menu': "እንኳዕ ብደሓን ናብ ወግዓዊ መሸጢ ቦት <b>'መዘምራን ልደታ ማርያም ቁምስና መቐለ'</b> ራብዓይ ኣልበም መጻእካ።",
        'buy_album_button': "🛒 ኣልበም ግዛእ",
        'about_album_button': "ℹ️ ብዛዕባ እዚ ኣልበም",
        'back_button': "🔙 ናብ መጀመርታ ተመለስ",
        'payment_instructions': (
            "ጽቡቕ! ዋጋ ኣልበም <b>{album_price} ብር</b> እዩ።\n\n"
            "ክፍሊት ንምፍጻም በዞም ዝስዕቡ ኣማራጺታት ተጠቐም፦\n\n"
            "<b><u>1. ንግዲ ባንክ ኢትዮጵያ (CBE):</u></b>\n"
            "<b>ስም:</b> ማሕበር መዘምራን ልደታ ማርያም ቁ.መቐለ\n"
            "<b>ቁጽሪ ሕሳብ:</b> 1000639550323\n\n"
            "<b><u>2. ባንኪ ኣቢሲንያ (BOA):</u></b>\n"
            "<b>ስም:</b> ማሕበር መዘምራን ልደታ ማርያም\n"
            "<b>ቁጽሪ ሕሳብ:</b> 196302506\n\n"
            "⚠️ <b>ኣገዳሲ:</b> ክፍሊት ምስ ፈጸምካ፡ ነቲ ደረሰኝ (screenshot) ናብ ኣካያዲና @Dmtsibereket ብምስዳድ ብኡንብኡ ናይ መእተዊ መላግቦ ክንሰደልካ ኢና።"
        ),
        'about_album_text': (
            "<b><u>ብዛዕባ ራብዓይ ኣልበም</u></b>\n\n"
            "እዚ ብ'መዘምራን ልደታ ማርያም ቁምስና መቐለ' ዝተዳለወ ራብዓይ ኣልበም ኮይኑ፡ "
            "ብዙሓት ሓደሽቲን መንፈሳውያን መዝሙራትን ዝሓዘ እዩ።\n\n"
            "<i>(ኣብዚ ተወሰኺ ሓበሬታ ወይ ዝርዝር መዝሙራት ክንውስኽ ንኽእል ኢና።)</i>"
        ),
        'saho_unavailable': "እቲ ናይ ሳሆ (ኢሮብ) ቋንቋ ክፋል ኣብ ስራሕ ይርከብ። በጃኻ ንግዚኡ ካልእ ቋንቋ ምረጽ።",
        'payment_received_admin': "ሓድሽ ናይ ክፍያ ደረሰኝ ካብ ተጠቃሚ {user_mention} (ID: `{user_id}`) ተቐቢልና ኣለና። በጃኻ ኣረጋግጽ።",
        'approve_usage': "ኣጠቓቕማ: /approve <user_id>\nኣብነት: /approve 123456789",
        'approval_success_admin': "✅ ብዓወት ተፈጺሙ! ናይ መእተዊ መላግቦ ናብ ተጠቃሚ {user_id} ተላኢኹ ኣሎ።",
        'approval_not_admin': "❌ ይቕሬታ፡ እዚ ትእዛዝ'ዚ በቲ ዝተመዘገበ ኣካያዲ ጥራይ እዩ ዝሰርሕ።",
        'payment_success_user': (
            "✅ <b>ክፍሊትኩም ብዓወት ተረጋጊጹ እዩ!</b> ✅\n\n"
            "ንዝገበርኩምልና ደገፍ ኣዚና ነምስግን።\n\n"
            "ነዚ ሓደ ግዜ ጥራይ ዝሰርሕ መላግቦ ተጠቒምኩም ናብቲ መዝሙራት ዘለዎ ቻነል ክትኣትዉ ትኽእሉ ኢኹም፦\n"
            "<b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቕሬታ፡ ነቲ ዝሰደድካዮ ናይ ክፍያ ደረሰኝ ከነረጋግጽ ኣይከኣልናን። በጃኻ ምስ @Dmtsibereket ተራኸብ።",
        'rejection_success_admin': "ንተጠቃሚ {user_id} ክፍሊቱ ከም ዘይተረጋገጸ ተነጊርዎ ኣሎ።",
    },
'am': {
        'welcome': "እንኳን ደህና መጡ <b>{user_name}</b>!\n\nእባክዎ ቋንቋ ይምረጡ:",
        'main_menu': "እንኳን ወደ <b>'የልደታ ማርያም መዘምራን ቁምስና መቀሌ'</b> አራተኛ አልበም ይፋዊ መሸጫ ቦት በደህና መጡ።",
        'buy_album_button': "🛒 አልበሙን ይግዙ",
        'about_album_button': "ℹ️ ስለ አልበሙ",
        'back_button': "🔙 ወደ ዋናው ምናሌ ይመለሱ",
        'payment_instructions': (
            "በጣም ጥሩ! የአልበሙ ዋጋ <b>{album_price} ብር</b> ነው።\n\n"
            "ክፍያ ለመፈጸም ከሚከተሉት አማራጮች ውስጥ አንዱን ይጠቀሙ፦\n\n"
            "<b><u>1. የኢትዮጵያ ንግድ ባንክ (CBE):</u></b>\n"
            "<b>ስም:</b> ማህበር መዘምራን ልደታ ማርያም ቁ.መቀሌ\n"
            "<b>የሂሳብ ቁጥር:</b> 1000639550323\n\n"
            "<b><u>2. አቢሲንያ ባንክ (BOA):</u></b>\n"
            "<b>ስም:</b> ማህበር መዘምራን ልደታ ማርያም\n"
            "<b>የሂሳብ ቁጥር:</b> 196302506\n\n"
            "⚠️ <b>አስፈላጊ:</b> ክፍያ ከፈጸሙ በኋላ፣ የክፍያ ማረጋገጫውን (screenshot) ለአስተዳዳሪያችን @Dmtsibereket በመላክ የመግቢያ ሊንክዎን ወዲያውኑ ይቀበላሉ።"
        ),
        'about_album_text': (
            "<b><u>ስለ አራተኛው አልበም</u></b>\n\n"
            "ይህ በ'የልደታ ማርያም መዘምራን ቁምስና መቀሌ' የተዘጋጀ አራተኛ አልበም ሲሆን፣ "
            "በርካታ አዳዲስና መንፈሳዊ መዝሙሮችን የያዘ ነው።\n\n"
            "<i>(ተጨማሪ መረጃ ወይም የዝማሬ ዝርዝር እዚህ ሊጨመር ይችላል።)</i>"
        ),
        'saho_unavailable': "የሳሆ (ኢሮብ) ቋንቋ ክፍል በግንባታ ላይ ነው። እባክዎ ለጊዜው ሌላ ቋንቋ ይምረጡ።",
        'payment_received_admin': "አዲስ የክፍያ ማረጋገጫ ከተጠቃሚ {user_mention} (ID: `{user_id}`) ደርሶናል። እባክዎ ያረጋግጡ።",
        'approve_usage': "አጠቃቀም: /approve <user_id>\nምሳሌ: /approve 123456789",
        'approval_success_admin': "✅ በተሳካ ሁኔታ ተፈጽሟል! የመግቢያ ሊንክ ለተጠቃሚ {user_id} ተልኳል።",
        'approval_not_admin': "❌ ይቅርታ፣ ይህ ትዕዛዝ በተመደበው አስተዳዳሪ ብቻ ነው የሚሰራው።",
        'payment_success_user': (
            "✅ <b>ክፍያዎ በተሳካ ሁኔታ ተረጋግጧል!</b> ✅\n\n"
            "ስለ ድጋፍዎ በጣም እናመሰግናለን።\n\n"
            "ይህን የአንድ ጊዜ አገልግሎት ብቻ የሚሰጥ ሊንክ በመጠቀም ወደ መዝሙሮቹ ቻናል መቀላቀል ይችላሉ፦\n"
            "<b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቅርታ፣ የላኩትን የክፍያ ማረጋገጫ ማረጋገጥ አልቻልንም። ለእርዳታ እባክዎ @Dmtsibereket ያግኙ።",
        'rejection_success_admin': "ለተጠቃሚ {user_id} ክፍያው እንዳልተረጋገጠ ተነግሮታል።",
    },
    'saho': {
        'welcome': "Bade Welcome, {user_name}!\n\Fadlan afki dooro:",
        'main_menu': "Welcome to the official sales bot for 'Lideta Mariam Choir Vol. 4' album.", # Needs Translation
        'buy_album_button': "🛒 Album Gid", # Needs Translation
        'about_album_button': "ℹ️ Ta Album Bica", # Needs Translation
        'back_button': "🔙 Ifi Gudfanah Dagca", # Needs Translation
        'payment_instructions': "Tani Part Ab Sereh We-et Yerkeb.", # Custom Message
        'about_album_text': "Tani Part Ab Sereh We-et Yerkeb.", # Custom Message
        'saho_unavailable': "Saho (Irob) afki-yi qism ab sereh we-et yerkeb. Fadlan, Gize-yu, Akak Af dooro.", # Placeholder
        # Admin and other technical messages can default to English for now
        'payment_received_admin': "New payment slip received from user {user_mention} (ID: `{user_id}`). Please verify.",
        'approve_usage': "Usage: /approve <user_id>\nExample: /approve 123456789",
        'approval_success_admin': "✅ Success! Invite link has been sent to user {user_id}.",
        'approval_not_admin': "❌ Sorry, this command can only be used by the designated admin.",
        'payment_success_user': (
            "✅ <b>Your payment has been successfully verified!</b> ✅\n\n"
            "You can now join the private channel using this one-time invite link:\n"
            "<b>{invite_link}</b>" # This can be translated
        ),
        'payment_rejected_user': "❌ We are sorry, but there was an issue verifying your payment slip. Please contact @Dmtsibereket for assistance.",
        'rejection_success_admin': "User {user_id} has been notified about the payment rejection.",
    }
}