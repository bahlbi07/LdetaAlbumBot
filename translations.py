# translations.py

TRANSLATIONS = {
    'en': {
        'welcome_language': "Welcome <b>{user_name}</b>!\n\nPlease choose your language to continue:",
        'ask_location': "Thank you for choosing English.\n\nPlease select your location:",
        'location_in_button': "🇪🇹 Inside Ethiopia",
        'location_out_button': "🌍 Outside Ethiopia",
        'welcome_main': (
            "Welcome to the official sales bot for the 4th album of the\n"
            "<b>'Lideta Mariam Choir, Qumsna Mekelle'</b>."
        ),
        'buy_album_button': "🛒 Purchase Album",
        'about_album_button': "ℹ️ About This Album",
        'back_to_start_button': "⬅️ Back to Language Select",
        'back_to_main_menu_button': "⬅️ Back to Main Menu",
        'slip_sent_button': "✅ I have sent the payment slip",
        'payment_instructions': (
            "Excellent choice! The price of the album is <b>{album_price} ETB</b>.\n\n"
            "To complete your purchase, please use one of the following methods:\n\n"
            "<b><u>1. Commercial Bank of Ethiopia (CBE):</u></b>\n"
            "<b>Account Name:</b> [YOUR_CBE_ACCOUNT_NAME_HERE]\n"
            "<b>Account Number:</b> [YOUR_CBE_ACCOUNT_NUMBER_HERE]\n\n"
            "<b><u>2. Bank of Abyssinia (BOA):</u></b>\n"
            "<b>Account Name:</b> [YOUR_BOA_ACCOUNT_NAME_HERE]\n"
            "<b>Account Number:</b> [YOUR_BOA_ACCOUNT_NUMBER_HERE]\n\n"
            "⚠️ <b>VERY IMPORTANT:</b> After you have made the payment, you **MUST** send the receipt (screenshot) to our admin at [@YOUR_ADMIN_USERNAME_HERE].\n\n"
            "Once you have sent the slip, please press the button below."
        ),
        'about_album_text': (
            "<b><u>About the 4th Album</u></b>\n\n"
            "This is the fourth album by the 'Lideta Mariam Choir, Qumsna Mekelle', "
            "filled with new and spiritually uplifting hymns. Your purchase is a great support for our ministry.\n\n"
            "Thank you and God bless you."
        ),
        'saho_unavailable': "The Saho (Irob) language section is currently under construction. Please choose another language for now.",
        'wait_for_verification': "Thank you! We have received your confirmation. An admin will now verify your payment slip. You will receive a message with the album link shortly. Please be patient.",
        'payment_notif_admin': "🔔 New Payment Slip Sent!\n\nUser {user_mention} (ID: `{user_id}`) has confirmed they sent a payment slip. Please check your messages from this user and verify the payment.\n\nOnce verified, use:\n`/approve {user_id}`\n\nIf the payment is invalid, use:\n`/reject {user_id}`",
        'approve_usage': "⚠️ Incorrect Usage!\nUse: /approve <user_id>\nExample: /approve 123456789",
        'reject_usage': "⚠️ Incorrect Usage!\nUse: /reject <user_id>\nExample: /reject 123456789",
        'approval_success_admin': "✅ Success! Invite link has been sent to user {user_id}.",
        'rejection_success_admin': "✅ Rejection notice has been sent to user {user_id}.",
        'approval_not_admin': "❌ Access Denied! This command is for admins only.",
        'payment_success_user': (
            "✅ <b>Your payment has been successfully verified!</b> ✅\n\n"
            "Thank you so much for your support. We pray that these hymns bring blessings to your life.\n\n"
            "You can now join the private channel using this **one-time** invite link:\n"
            "<b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ We are sorry, but there was an issue verifying your payment. Your request has been declined. If you believe this is a mistake, please contact our admin directly at [@YOUR_ADMIN_USERNAME_HERE] for assistance.",
    },
    'ti': {
        'welcome_language': "ሰላም <b>{user_name}</b>! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ንኽትቅጽል ቋንቋ ምረጽ፦",
        'ask_location': "ቋንቋ ትግርኛ መሪጽካ ኣለኻ።\n\nበጃኻ ኣበይ ከም ዘለኻ ምረጽ፦",
        'location_in_button': "🇪🇹 ኣብ ውሽጢ ኢትዮጵያ",
        'location_out_button': "🌍 ካብ ኢትዮጵያ ወጻኢ",
        'welcome_main': (
            "እንኳዕ ብደሓን ናብ ወግዓዊ መሸጢ ቦት ናይ'ቲ ራብዓይ ኣልበም ናይ\n"
            "<b>'መዘምራን ልደታ ማርያም ቁምስና መቐለ'</b>"
        ),
        'buy_album_button': "🛒 ኣልበም ግዛእ",
        'about_album_button': "ℹ️ ብዛዕባ እዚ ኣልበም",
        'back_to_start_button': "⬅️ ናብ ቋንቋ ምምራጽ ተመለስ",
        'back_to_main_menu_button': "⬅️ ናብ ቀንዲ ገጽ ተመለስ",
        'slip_sent_button': "✅ ነቲ ደረሰኝ ለኣኸዮ ኣለኹ",
        'payment_instructions': (
            "ብሉጽ ምርጫ! ዋጋ ናይ'ዚ ኣልበም <b>{album_price} ብር</b> እዩ።\n\n"
            "ክፍሊት ንምፍጻም በዞም ዝስዕቡ ኣገባባት ተጠቐም፦\n\n"
            "<b><u>1. ንግዲ ባንክ ኢትዮጵያ (CBE):</u></b>\n"
            "<b>ስም:</b> [YOUR_CBE_ACCOUNT_NAME_HERE]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [YOUR_CBE_ACCOUNT_NUMBER_HERE]\n\n"
            "<b><u>2. ባንኪ ኣቢሲንያ (BOA):</u></b>\n"
            "<b>ስም:</b> [YOUR_BOA_ACCOUNT_NAME_HERE]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [YOUR_BOA_ACCOUNT_NUMBER_HERE]\n\n"
            "⚠️ <b>ኣዝዩ ኣገዳሲ:</b> ክፍሊትካ ምስ ፈጸምካ፡ ነቲ ደረሰኝ (screenshot) ናብ ኣካያዲና [@YOUR_ADMIN_USERNAME_HERE] ክትሰዶ **ግድን** እዩ።\n\n"
            "ነቲ ደረሰኝ ምስ ሰደድካዮ፡ ነዛ ኣብ ታሕቲ ዘላ ቁልፊ ጠውቕ።"
        ),
        'about_album_text': (
            "<b><u>ብዛዕባ ራብዓይ ኣልበም</u></b>\n\n"
            "እዚ ብ'መዘምራን ልደታ ማርያም ቁምስና መቐለ' ዝተዳለወ ራብዓይ ኣልበም ኮይኑ፡ "
            "ብዙሓት ሓደሽቲን መንፈሳውያን መዝሙራትን ዝሓዘ እዩ። ምዕዳግካ ንኣገልግሎትና ዓቢ ደገፍ እዩ።\n\n"
            "የቐንየልና! እግዚኣብሔር ይባርኽካ።"
        ),
        'saho_unavailable': "እቲ ናይ ሳሆ (ኢሮብ) ቋንቋ ክፋል ኣብ ስራሕ ይርከብ። በጃኻ ንግዚኡ ካልእ ቋንቋ ምረጽ።",
        'wait_for_verification': "የቐንየልና!  መረጋገጺ ተቐቢልና ኣለና። ሓደ ኣካያዲ ሕጂ ነቲ ዝሰደድካዮ ደረሰኝ ከረጋግጾ እዩ። ድሕሪ ቁሩብ እዋን ናይ መእተዊ መላግቦ ክንሰደልካ ኢና። በጃኻ ብትዕግስቲ ጽናሕ።",
        'payment_notif_admin': "🔔 ሓድሽ ደረሰኝ ተላኢኹ!\n\nተጠቃሚ {user_mention} (ID: `{user_id}`) ደረሰኝ ከም ዝለኣኸ ኣፍሊጡ ኣሎ። በጃኻ ናብዚ ሰብ'ዚ ዝመጸካ መልእኽቲ ርኢኻ ነቲ ክፍሊት ኣረጋግጽ።\n\nምስ ኣረጋገጽካ:\n`/approve {user_id}`\n\nክፍሊቱ ጌጋ እንተኾይኑ:\n`/reject {user_id}`",
        'approve_usage': "⚠️ ጌጋ ኣጠቓቕማ!\nከምዚ ተጠቐም: /approve <user_id>\nኣብነት: /approve 123456789",
        'reject_usage': "⚠️ ጌጋ ኣጠቓቕማ!\nከምዚ ተጠቐም: /reject <user_id>\nኣብነት: /reject 123456789",
        'approval_success_admin': "✅ ብዓወት ተፈጺሙ! ናይ መእተዊ መላግቦ ናብ ተጠቃሚ {user_id} ተላኢኹ ኣሎ።",
        'rejection_success_admin': "✅ ንተጠቃሚ {user_id} ክፍሊቱ ከም ዘይተረጋገጸ መልእኽቲ ተላኢኽዎ ኣሎ።",
        'approval_not_admin': "❌ ፍቓድ የብልካን! እዚ ትእዛዝ'ዚ ንኣካየድቲ ጥራይ እዩ።",
        'payment_success_user': (
            "✅ <b>ክፍሊትኩም ብዓወት ተረጋጊጹ እዩ!</b> ✅\n\n"
            "ንዝገበርኩምልና ደገፍ ኣዚና ነምስግን። እዞም መዝሙራት በረኸት ከምጽኡልኩም ንምነ።\n\n"
            "ነዚ **ሓደ ግዜ ጥራይ** ዝሰርሕ መላግቦ ተጠቒምኩም ናብቲ ውሑስ ቻነል ክትኣትዉ ትኽእሉ ኢኹም፦\n"
            "<b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቕሬታ፡ ነቲ ዝሰደድካዮ ደረሰኝ ከነረጋግጽ ኣይከኣልናን። ሕቶኻ ተነጺጉ ኣሎ። እዚ ብጌጋ ዝተፈጸመ ይመስለካ እንተኾይኑ፡ በጃኻ ምስ ኣካያዲና ብቐጥታ ኣብ [@YOUR_ADMIN_USERNAME_HERE] ተራኸብ።",
    },
    'am': {
        'welcome_language': "ሰላም <b>{user_name}</b>! እንኳን ደህና መጡ።\n\nእባክዎ ለመቀጠል ቋንቋ ይምረጡ:",
        'ask_location': "የአማርኛ ቋንቋ መርጠዋል።\n\nእባክዎ አሁን ያሉበትን ቦታ ይምረጡ:",
        'location_in_button': "🇪🇹 በኢትዮጵያ ውስጥ",
        'location_out_button': "🌍 ከኢትዮጵያ ውጪ",
        'welcome_main': (
            "እንኳን ወደ <b>'የልደታ ማርያም መዘምራን ቁምስና መቀሌ'</b> አራተኛ አልበም ይፋዊ መሸጫ ቦት በደህና መጡ።"
        ),
        'buy_album_button': "🛒 አልበሙን ይግዙ",
        'about_album_button': "ℹ️ ስለ አልበሙ",
        'back_to_start_button': "⬅️ ወደ ቋንቋ ምርጫ ይመለሱ",
        'back_to_main_menu_button': "⬅️ ወደ ዋናው ምናሌ ይመለሱ",
        'slip_sent_button': "✅ የክፍያ ማረጋገጫውን ልኬያለሁ",
        'payment_instructions': (
            "በጣም ጥሩ! የአልበሙ ዋጋ <b>{album_price} ብር</b> ነው።\n\n"
            "ክፍያ ለመፈጸም ከሚከተሉት መንገዶች አንዱን ይጠቀሙ፦\n\n"
            "<b><u>1. የኢትዮጵያ ንግድ ባንክ (CBE):</u></b>\n"
            "<b>ስም:</b> [YOUR_CBE_ACCOUNT_NAME_HERE]\n"
            "<b>የሂሳብ ቁጥር:</b> [YOUR_CBE_ACCOUNT_NUMBER_HERE]\n\n"
            "<b><u>2. አቢሲንያ ባንክ (BOA):</u></b>\n"
            "<b>ስም:</b> [YOUR_BOA_ACCOUNT_NAME_HERE]\n"
            "<b>የሂሳብ ቁጥር:</b> [YOUR_BOA_ACCOUNT_NUMBER_HERE]\n\n"
            "⚠️ <b>በጣም አስፈላጊ:</b> ክፍያ ከፈጸሙ በኋላ፣ የክፍያ ማረጋገጫውን (screenshot) ለአስተዳዳሪያችን [@YOUR_ADMIN_USERNAME_HERE] መላክ **ግዴታ** ነው።\n\n"
            "ደረሰኙን ከላኩ በኋላ፣ ከታች ያለውን ቁልፍ ይጫኑ።"
        ),
        'about_album_text': (
            "<b><u>ስለ አራተኛው አልበም</u></b>\n\n"
            "ይህ በ'የልደታ ማርያም መዘምራን ቁምስና መቀሌ' የተዘጋጀ አራተኛ አልበም ሲሆን፣ "
            "በርካታ አዳዲስና መንፈሳዊ መዝሙሮችን ይዟል። ግዢዎ ለአገልግሎታችን ትልቅ ድጋፍ ነው።\n\n"
            "እናመሰግናለን! እግዚአብሔር ይባርክዎ።"
        ),
        'saho_unavailable': "ገና በስራ ላይ ስለ ሆነ ሌሎችን ኣማራጮች ይመልከቱ",
        'wait_for_verification': "እናመሰግናለን! ማረጋገጫዎን ተቀብለናል። አስተዳዳሪ አሁን የክፍያ ወረቀትዎን ያረጋግጣል። የመግቢያ ሊንክ ያለው መልእክት በቅርቡ ይደርስዎታል። እባክዎ በትዕግስት ይጠብቁ።",
        'payment_notif_admin': "🔔 አዲስ የክፍያ ማረጋገጫ ተልኳል!\n\nተጠቃሚ {user_mention} (ID: `{user_id}`) የክፍያ ወረቀት መላኩን አረጋግጧል። እባክዎ ከዚህ ተጠቃሚ የመጡትን መልዕክቶች ያረጋግጡ እና ክፍያውን ያረጋግጡ።\n\nአንዴ ካረጋገጡ በኋላ ይጠቀሙ:\n`/approve {user_id}`\n\nክፍያው ልክ ያልሆነ ከሆነ ይጠቀሙ:\n`/reject {user_id}`",
        'approve_usage': "⚠️ የተሳሳተ አጠቃቀም!\nይህን ይጠቀሙ: /approve <user_id>\nምሳሌ: /approve 123456789",
        'reject_usage': "⚠️ የተሳሳተ አጠቃቀም!\nይህን ይጠቀሙ: /reject <user_id>\nምሳሌ: /reject 123456789",
        'approval_success_admin': "✅ ተሳክቷል! የመግቢያ ሊንክ ለተጠቃሚ {user_id} ተልኳል።",
        'rejection_success_admin': "✅ ለተጠቃሚ {user_id} ክፍያው ውድቅ መደረጉ ተነግሮታል።",
        'approval_not_admin': "❌ ፍቃድ የለዎትም! ይህ ትዕዛዝ ለአስተዳዳሪዎች ብቻ ነው።",
        'payment_success_user': (
            "✅ <b>ክፍያዎ በተሳካ ሁኔታ ተረጋግጧል!</b> ✅\n\n"
            "ስለ ድጋፍዎ በጣም እናመሰግናለን። እነዚህ መዝሙሮች ለህይወትዎ በረከትን እንዲያመጡ እንጸልያለን።\n\n"
            "ይህን **የአንድ ጊዜ** መግቢያ ሊንክ በመጠቀም ወደ ግል ቻናሉ መቀላቀል ይችላሉ፦\n"
            "<b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቅርታ፣ ክፍያዎን ማረጋገጥ ላይ ችግር ነበር። ጥያቄዎ ውድቅ ተደርጓል። ይህ በስህተት እንደሆነ ካመኑ፣ እባክዎ አስተዳዳሪያችንን በቀጥታ በ [@YOUR_ADMIN_USERNAME_HERE] ያግኙ።",
    },
    'saho': {
        'welcome_language': "Bade Welcome, <b>{user_name}</b>!\n\nFadlan afki dooro:",
        'ask_location': "Saho afki dortotte.\n\nFadlan, abey Rammah Anitto dooro:",
        'location_in_button': "🇪🇹 Ethiopia Gudul",
        'location_out_button': "🌍 Ethiopia Badaak",
        'welcome_main': "Tani Qism Ab Sereh We-et Yerkeb. (This section is under construction).",
        'buy_album_button': "🛒 Album Gid (Under Const.)",
        'about_album_button': "ℹ️ Ta Album Bica (Under Const.)",
        'back_to_start_button': "⬅️ Ifi Af Dorrole Dagca",
        'back_to_main_menu_button': "⬅️ Ifi Gudfanah Dagca",
        'slip_sent_button': "✅ Derese Aka Le Ake.",
        'payment_instructions': "Tani qism ab sereh we-et yerkeb. Fadlan akak af dooro.",
        'about_album_text': "Tani qism ab sereh we-et yerkeb.",
        'saho_unavailable': "እዚ ክፋል ናይ ሳሆ ኣብ ስራሕ እዩ ዝርከብ በይዛኦም ንግዚኡ ካሊእ ቋንቋ ይጠቀሙ።",
        'wait_for_verification': "Shukran! Tenna potvrijedženje tergabne. Admin hiyye tenna derese karagagse. Ba-adoh Gizek na kanal adagsele link kalakna. Fadlan bi tigisti sanaah.",
        # Admin and other messages will use English as a fallback
        'payment_success_user': (
            "✅ <b>Kiflitotoh Bi Awot Teragagitse!</b> ✅\n\n"
            "Dagaf-oh abissinnah, azinne namisgin.\n\n"
            "Tani **ide gezeh** takaddam link kah dagoytiyok na channel kadato takale:-\n"
            "<b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ Ikra! Tenna kiflitot derese karagagne akeennino. Fadlan na admin bi qeteta ab [@YOUR_ADMIN_USERNAME_HERE] terakeb.",
    }
}