# translations.py

TRANSLATIONS = {
    # ====================================================================================
    # English Translations
    # ====================================================================================
    'en': {
        'welcome_language': "Welcome <b>{user_name}</b>!\n\nPlease choose your language to continue:",
        'main_menu': (
            "Welcome to the official digital store for the albums of the\n"
            "<b>'Lideta Mariam Choir, Qumsna Mekelle'</b>.\n\n"
            "Please select an album to purchase:"
        ),
        'album_vol_4': "Eyesus (Vol. 4) - 300 ETB",
        'album_vol_3': "Ne'aka Amina (Vol. 3) - 100 ETB",
        'album_vol_2': "Tesfa Alona (Vol. 2) - 100 ETB",
        'album_vol_1': "Kezimrelka (Vol. 1) - 100 ETB",
        'how_to_buy_button': "📖 How to Buy Guide",
        'back_to_main_menu_button': "⬅️ Back to Album List",
        'home_button': "🏠 Back to Main Menu",
        'help_button': "❔ Help",
        'ask_payment_method': "Please confirm your payment method.\nSend the **Transaction ID** as a text message, or send the **Payment Slip (Screenshot)** as a photo.",
        'payment_instructions': (
            "Excellent choice! You are purchasing <b>{album_title}</b> for <b>{album_price} ETB</b>.\n\n"
            "To complete your purchase, please use one of the following methods:\n\n"
            "<b><u>1. Commercial Bank of Ethiopia (CBE):</u></b>\n"
            "<b>Name:</b> [YOUR_CBE_ACCOUNT_NAME_HERE]\n"
            "<b>Account Number:</b> [YOUR_CBE_ACCOUNT_NUMBER_HERE]\n\n"
            "<b><u>2. Bank of Abyssinia (BOA):</u></b>\n"
            "<b>Name:</b> [YOUR_BOA_ACCOUNT_NAME_HERE]\n"
            "<b>Account Number:</b> [YOUR_BOA_ACCOUNT_NUMBER_HERE]\n\n"
            "⚠️ <b>VERY IMPORTANT:</b>\n"
            "After paying, please come back here and send us the **Transaction ID** (e.g., `ET123...`) or the payment **Screenshot**."
        ),
        'location_out_unavailable': "Service for customers outside Ethiopia is currently under construction. We apologize for the inconvenience.",
        'help_text_main': "<b>GUIDE:</b> This is the main menu. You can select any album to start the purchase process. If you need a detailed guide, click the 'How to Buy Guide' button.",
        'help_text_payment': "<b>GUIDE:</b> On this page, please make your payment using the provided bank details. Afterwards, you must send either the Transaction ID (as text) or the payment slip (as a photo) to this bot to proceed.",
        'slip_received': "Thank you! We have received your payment information. An admin will now verify it. This may take some time. You will receive a notification as soon as it is approved. Please be patient.",
        'payment_notif_admin': (
            "🔔 **New Payment Submission!** 🔔\n\n"
            "<b>User:</b> {user_mention} (ID: `{user_id}`)\n"
            "<b>Album:</b> {album_title}\n\n"
            "The user has submitted payment information. Please check your direct messages from them for the Transaction ID or Screenshot and verify the payment.\n\n"
            "➡️ To approve: Click `/approve {user_id} {album_key}`\n"
            "➡️ To reject: Click `/reject {user_id}`"
        ),
        'approve_usage': "⚠️ **Incorrect Usage!**\nUse: `/approve <user_id> <album_key>`\nExample: `/approve 123456789 vol4`",
        'reject_usage': "⚠️ **Incorrect Usage!**\nUse: `/reject <user_id>`\nExample: `/reject 123456789`",
        'approval_success_admin': "✅ Success! Invite link for <b>{album_title}</b> has been sent to user {user_id}.",
        'rejection_success_admin': "✅ Rejection notice has been sent to user {user_id}.",
        'approval_not_admin': "❌ Access Denied! This command is for the admin only.",
        'payment_success_user': (
            "🎉 **Congratulations! Your payment is verified!** 🎉\n\n"
            "Thank you for purchasing <b>{album_title}</b>. Your support for our ministry is deeply appreciated.\n\n"
            "Click the link below to join the private channel. This is a **one-time** use link.\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ We are sorry, but there was an issue verifying your payment. Your request has been declined. If you believe this is a mistake, please contact our admin directly at [@YOUR_ADMIN_USERNAME_HERE] for assistance.",
        'feedback_prompt': "We hope you are being blessed by the hymns! In a few days, we will send you a message asking for your thoughts and feedback on the album.",
        'feedback_request': "Hello {user_name}! We hope you have enjoyed the <b>{album_title}</b> album. We would be grateful if you could share your feedback or testimony with us. Your words are a great encouragement!",
    },

    # ====================================================================================
    # Tigrinya Translations
    # ====================================================================================
    'ti': {
        'welcome_language': "ሰላም <b>{user_name}</b>! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ንኽትቅጽል ቋንቋ ምረጽ፦",
        'main_menu': (
            "እንኳዕ ብደሓን ናብ ወግዓዊ ዲጂታል መሸጢ ናይ ኣልበማት\n"
            "<b>'መዘምራን ልደታ ማርያም ቁምስና መቐለ'</b> በጻሕካ።\n\n"
            "በጃኻ ክትዕድግ እትደሊ ኣልበም ምረጽ፦"
        ),
        'album_vol_4': "እየሱስ (Vol. 4) - 300 ብር",
        'album_vol_3': "ንዓኻ ኣሚና (Vol. 3) - 100 ብር",
        'album_vol_2': "ተስፋ ኣሎና (Vol. 2) - 100 ብር",
        'album_vol_1': "ክዝምረልካ (Vol. 1) - 100 ብር",
        'how_to_buy_button': "📖 ኣገባብ ኣተዓዳድጋ",
        'back_to_main_menu_button': "⬅️ ናብ ዝርዝር ኣልበማት ተመለስ",
        'home_button': "🏠 ናብ ቀንዲ ገጽ",
        'help_button': "❔ ሓገዝ",
        'ask_payment_method': "በጃኻ ናይ ክፍያ መረጋገጺ ኣገባብካ ምረጽ።\nነቲ **Transaction ID** ከም ጽሑፍ፡ ወይ ነቲ **ናይ ክፍያ ደረሰኝ (Screenshot)** ከም ስእሊ ስደድ።",
        'payment_instructions': (
            "ብሉጽ ምርጫ! ንስኻ <b>{album_title}</b> ብ<b>{album_price} ብር</b> ትዕድግ ኣለኻ።\n\n"
            "ክፍሊት ንምፍጻም በዞም ዝስዕቡ ኣገባባት ተጠቐም፦\n\n"
            "<b><u>1. ንግዲ ባንክ ኢትዮጵያ (CBE):</u></b>\n"
            "<b>ስም:</b> [YOUR_CBE_ACCOUNT_NAME_HERE]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [YOUR_CBE_ACCOUNT_NUMBER_HERE]\n\n"
            "<b><u>2. ባንኪ ኣቢሲንያ (BOA):</u></b>\n"
            "<b>ስም:</b> [YOUR_BOA_ACCOUNT_NAME_HERE]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [YOUR_BOA_ACCOUNT_NUMBER_HERE]\n\n"
            "⚠️ <b>ኣዝዩ ኣገዳሲ:</b>\n"
            "ክፍሊትካ ምስ ፈጸምካ፡ ናብዚ ተመሊስካ ነቲ **Transaction ID** (ንኣብነት፡ `ET123...`) ወይ ነቲ **Screenshot** ክትሰደልና ኣለካ።"
        ),
        'location_out_unavailable': "ንደንበኛታትና ኣብ ወጻኢ ዚኸውን ኣገልግሎት ኣብዚ እዋን'ዚ ኣብ ስራሕ ይርከብ። ንዘጋጠመ ምድንጓይ ይቕሬታ ንሓትት።",
        'help_text_main': "<b>መርሒ:</b> እዚ ቀንዲ ገጽ እዩ። ዝኾነ ኣልበም መሪጽካ ናይ ምዕዳግ መስርሕ ክትጅምር ትኽእል ኢኻ። ዝርዝር መምርሒ እንተደሊኻ፡ 'ኣገባብ ኣተዓዳድጋ' ዝብል ቁልፊ ጠውቕ።",
        'help_text_payment': "<b>መርሒ:</b> ኣብዚ ገጽ'ዚ፡ በቶም ዝተዋህቡ ናይ ባንክ ሓበሬታታት ተጠቒምካ ክፍሊትካ ፈጽም። ድሕሪኡ፡ ነቲ Transaction ID (כמו ጽሑፍ) ወይ ነቲ ደረሰኝ (כמו ስእሊ) ናብዚ ቦት'ዚ ክትሰዶ ኣለካ።",
        'slip_received': "የቐንየልና! ናይ ክፍያ ሓበሬታኻ ተቐቢልና ኣለና። ሓደ ኣካያዲ ሕጂ ከረጋግጾ እዩ። እዚ ቁሩብ ግዜ ክወስድ ይኽእል እዩ። ምስ ተረጋገጸ ብኡንብኡ መልእኽቲ ክንሰደልካ ኢና። በጃኻ ብትዕግስቲ ጽናሕ።",
        'payment_notif_admin': (
            "🔔 **ሓድሽ ናይ ክፍያ ሓበሬታ!** 🔔\n\n"
            "<b>ተጠቃሚ:</b> {user_mention} (ID: `{user_id}`)\n"
            "<b>ኣልበም:</b> {album_title}\n\n"
            "እዚ ተጠቃሚ'ዚ ናይ ክፍያ ሓበሬታ ሰዲዱ ኣሎ። በጃኻ ናብ ውልቃዊ መልእኽቱ ኬድካ ነቲ Transaction ID ወይ Screenshot ርኢኻ ኣረጋግጽ።\n\n"
            "➡️ ንምርግጋጽ: ኣብዚ ጠውቕ `/approve {user_id} {album_key}`\n"
            "➡️ ንምንጻግ: ኣብዚ ጠውቕ `/reject {user_id}`"
        ),
        'approve_usage': "⚠️ **ጌጋ ኣጠቓቕማ!**\nከምዚ ተጠቐም: `/approve <user_id> <album_key>`\nኣብነት: `/approve 123456789 vol4`",
        'reject_usage': "⚠️ **ጌጋ ኣጠቓቕማ!**\nከምዚ ተጠቐም: `/reject <user_id>`\nኣብነት: `/reject 123456789`",
        'approval_success_admin': "✅ ብዓወት ተፈጺሙ! ናይ መእተዊ መላግቦ ን <b>{album_title}</b> ናብ ተጠቃሚ {user_id} ተላኢኹ ኣሎ።",
        'rejection_success_admin': "✅ ንተጠቃሚ {user_id} ክፍሊቱ ከም ዘይተረጋገጸ መልእኽቲ ተላኢኽዎ ኣሎ።",
        'approval_not_admin': "❌ ፍቓድ የብልካን! እዚ ትእዛዝ'ዚ ንኣካየድቲ ጥራይ እዩ።",
        'payment_success_user': (
            "🎉 **እንኳዕ ደስ በለካ! ክፍሊትካ ብዓወት ተረጋጊጹ እዩ!** 🎉\n\n"
            "ን <b>{album_title}</b> ስለ ዝዓደግካ ኣዚና ነምስግን። እዞም መዝሙራት በረኸት ከምጽኡልካ ንምነ።\n\n"
            "ነዚ **ሓደ ግዜ ጥራይ** ዝሰርሕ መላግቦ ጠዊቕካ ናብቲ ውሑስ ቻነል ክትጽንበር ትኽእል ኢኻ፦\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቕሬታ፡ ነቲ ዝሰደድካዮ ናይ ክፍያ ሓበሬታ ከነረጋግጽ ኣይከኣልናን። ሕቶኻ ተነጺጉ ኣሎ። እዚ ብጌጋ ዝተፈጸመ ይመስለካ እንተኾይኑ፡ በጃኻ ምስ ኣካያዲና ብቐጥታ ኣብ [@YOUR_ADMIN_USERNAME_HERE] ተራኸብ።",
        'feedback_prompt': "እቶም መዝሙራት የበርኹኹም ከም ዘለዉ ተስፋ ንገብር! ድሕሪ ገለ መዓልታት፡ ሓሳብ ርኢቶኹም ንምሕታት መልእኽቲ ክንሰደልኩም ኢና።",
        'feedback_request': "ሰላም {user_name}! ነቲ ናይ <b>{album_title}</b> ኣልበም ከም እትሰምዖ ዘለኻ ተስፋ ንገብር። ሓሳብካ ወይ ምስክርነትካ እንተተካፍለና፡ ኣዚና ምተሓጎስና። ቃልካ ዓቢ መተባብዒ እዩ!",
    },

    # ====================================================================================
    # Amharic Translations
    # ====================================================================================
    'am': {
        'welcome_language': "ሰላም <b>{user_name}</b>! እንኳን ደህና መጡ።\n\nእባክዎ ለመቀጠל ቋንቋ ይምረጡ:",
        'main_menu': (
            "እንኳን ወደ <b>'የልደታ ማርያም መዘምራን ቁምስና መቀሌ'</b> ይፋዊ ዲጂታል የአልበም መሸጫ በደህና መጡ።\n\n"
            "እባክዎ መግዛት የሚፈልጉትን አልበም ይምረጡ፦"
        ),
        'album_vol_4': "ኢየሱስ (Vol. 4) - 300 ብር",
        'album_vol_3': "አንተን አምና (Vol. 3) - 100 ብር",
        'album_vol_2': "ተስፋ አለን (Vol. 2) - 100 ብር",
        'album_vol_1': "ልዘምርልህ (Vol. 1) - 100 ብር",
        'how_to_buy_button': "📖 እንዴት መግዛት ይቻላል",
        'back_to_main_menu_button': "⬅️ ወደ አልበሞች ዝርዝር ይመለሱ",
        'home_button': "🏠 ወደ ዋናው ምናሌ",
        'help_button': "❔ እርዳታ",
        'ask_payment_method': "እባክዎ የክፍያ ማረጋገጫ ዘዴዎን ይምረጡ።\n**Transaction ID**ውን እንደ ጽሑፍ ወይም **የክፍያ ደረሰኙን (Screenshot)** እንደ ፎቶ ይላኩ።",
        'payment_instructions': (
            "በጣም ጥሩ ምርጫ! እርስዎ <b>{album_title}</b>ን በ<b>{album_price} ብር</b> እየገዙ ነው።\n\n"
            "ክፍያ ለመፈጸም ከሚከተሉት መንገዶች አንዱን ይጠቀሙ፦\n\n"
            "<b><u>1. የኢትዮጵያ ንግድ ባንክ (CBE):</u></b>\n"
            "<b>ስም:</b> [YOUR_CBE_ACCOUNT_NAME_HERE]\n"
            "<b>የሂሳብ ቁጥር:</b> [YOUR_CBE_ACCOUNT_NUMBER_HERE]\n\n"
            "<b><u>2. አቢሲንያ ባንክ (BOA):</u></b>\n"
            "<b>ስም:</b> [YOUR_BOA_ACCOUNT_NAME_HERE]\n"
            "<b>የሂሳብ ቁጥር:</b> [YOUR_BOA_ACCOUNT_NUMBER_HERE]\n\n"
            "⚠️ <b>በጣም አስፈላጊ:</b>\n"
            "ክፍያ ከፈጸሙ በኋላ፣ ወደዚህ በመመለስ የ**Transaction ID** (ለምሳሌ፡ `ET123...`) ወይም የክፍያ **Screenshot** መላክ አለብዎት።"
        ),
        'location_out_unavailable': "ከኢትዮጵያ ውጪ ላሉ ደንበኞች የሚሆን አገልግሎት በአሁኑ ሰዓት በግንባታ ላይ ነው። ስለተፈጠረው መዘግየት ይቅርታ እንጠይቃለን።",
        'help_text_main': "<b>መመሪያ:</b> ይህ ዋናው ገጽ ነው። የትኛውንም አልበም በመምረጥ የግዢ ሂደቱን መጀመር ይችላሉ። ዝርዝር መመሪያ ከፈለጉ 'እንዴት መግዛት ይቻላል' የሚለውን ቁልፍ ይጫኑ።",
        'help_text_payment': "<b>መመሪያ:</b> በዚህ ገጽ ላይ، በተሰጠው የባንክ መረጃ ተጠቅመው ክፍያዎን ይፈጽሙ። ከዚያ በኋላ، Transaction ID (በጽሑፍ) ወይም ደረሰኙን (በፎቶ) ወደዚህ ቦት መላክ አለብዎት።",
        'slip_received': "እናመሰግናለን! የክፍያ መረጃዎ ደርሶናል። አንድ አስተዳዳሪ አሁን ያረጋግጣል። ይህ የተወሰነ ጊዜ ሊወስድ ይችላል። ማረጋገጫ ሲያገኝ ወዲያውኑ መልእክት ይደርስዎታል። እባክዎ በትዕግስት ይጠብቁ።",
        'payment_notif_admin': (
            "🔔 **አዲስ የክፍያ መረጃ!** 🔔\n\n"
            "<b>ተጠቃሚ:</b> {user_mention} (ID: `{user_id}`)\n"
            "<b>አልበም:</b> {album_title}\n\n"
            "ይህ ተጠቃሚ የክፍያ መረጃ ልኳል። እባክዎ ወደ ግል መልእክቱ በመሄድ Transaction ID ወይም Screenshot দেখে ክፍያውን ያረጋግጡ።\n\n"
            "➡️ ለማጽደቅ: እዚህ ይጫኑ `/approve {user_id} {album_key}`\n"
            "➡️ ላለመቀበል: እዚህ ይጫኑ `/reject {user_id}`"
        ),
        'payment_success_user': (
            "🎉 **እንኳን ደስ አለዎት! ክፍያዎ በተሳካ ሁኔታ ተረጋግጧል!** 🎉\n\n"
            "<b>{album_title}</b>ን ስለገዙ በጣም እናመሰግናለን። ለአገልግሎታችን ላደረጉት ድጋፍ ከልብ እናመሰግናለን።\n\n"
            "ይህን **የአንድ ጊዜ** መግቢያ ሊንክ በመጫን ወደ ግል ቻናሉ መቀላቀል ይችላሉ፦\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቅርታ፣ የላኩትን የክፍያ መረጃ ማረጋገጥ አልቻልንም። ጥያቄዎ ውድቅ ተደርጓል። ይህ በስህተት እንደሆነ ካመኑ፣ እባክዎ አስተዳዳሪያችንን በቀጥታ በ [@YOUR_ADMIN_USERNAME_HERE] ያግኙ።",
        'feedback_prompt': "ዝማሬዎቹ እየባረኩዎት እንደሆነ ተስፋ እናደርጋለን! ከጥቂት ቀናት በኋላ፣ ስለ አልበሙ ያለዎትን አስተያየት ለመጠየቅ መልእክት እንልክልዎታለን።",
        'feedback_request': "ሰላም {user_name}! የ<b>{album_title}</b>ን አልበም እንደወደዱት ተስፋ እናደርጋለን። አስተያየትዎን ወይም ምስክርነትዎን ቢያካፍሉን በጣም እንደሰታለን። ቃልዎ ትልቅ ማበረታቻ ነው!",
    },

    # ====================================================================================
    # Afaan Oromoo Translations
    # ====================================================================================
    'om': {
        'welcome_language': "Baga nagaan dhuftan <b>{user_name}</b>!\n\nMaaloo itti fufuuf afaan filadhaa:",
        'main_menu': (
            "Gara bot gurgurtaa albamii arfaffaa\n"
            "<b>'Garee Mezemran Lideta Mariam Qumsna Maqalee'</b>-tti nagaan dhuftan.\n\n"
            "Maaloo albamii bitachuu barbaaddan filadhaa:"
        ),
        'album_vol_4': "Iyyasuus (Vol. 4) - 300 ETB",
        'album_vol_3': "Si Amannee (Vol. 3) - 100 ETB",
        'album_vol_2': "Abdii Qabna (Vol. 2) - 100 ETB",
        'album_vol_1': "Sin Faarsina (Vol. 1) - 100 ETB",
        'how_to_buy_button': "📖 Akkamitti Bittam",
        'back_to_main_menu_button': "⬅️ Gara Tarree Albamootaatti Deebi'i",
        'home_button': "🏠 Gara Fuula Jalqabaatti",
        'help_button': "❔ Gargaarsa",
        'ask_payment_method': "Maaloo tooftaa mirkaneessa kaffaltii keessanii filadhaa.\n**Lakkoofsa Raawwii** (Transaction ID) akka barruutti, ykn **Nagahee Kaffaltii (Screenshot)** akka suuraatti ergaa.",
        'payment_instructions': (
            "Filannoo gaarii! Albamii <b>{album_title}</b> gatii <b>{album_price} ETB</b>-tiin bitachaa jirtu.\n\n"
            "Kaffaltii raawwachuuf tooftaalee armaan gadii keessaa tokko fayyadamaa:\n\n"
            "<b><u>1. Baankii Daldalaa Itiyoophiyaa (CBE):</u></b>\n"
            "<b>Maqaa:</b> [YOUR_CBE_ACCOUNT_NAME_HERE]\n"
            "<b>Lak. Herreegaa:</b> [YOUR_CBE_ACCOUNT_NUMBER_HERE]\n\n"
            "<b><u>2. Baankii Abisiiniyaa (BOA):</u></b>\n"
            "<b>Maqaa:</b> [YOUR_BOA_ACCOUNT_NAME_HERE]\n"
            "<b>Lak. Herreegaa:</b> [YOUR_BOA_ACCOUNT_NUMBER_HERE]\n\n"
            "⚠️ <b>Hedduu Barbaachisaa:</b>\n"
            "Kaffaltii erga raawwattanii booda, as deebi'uun **Lakkoofsa Raawwii** (fkn, `ET123...`) ykn **Screenshot** kaffaltii nuuf erguu qabdu."
        ),
        'location_out_unavailable': "Tajaajilli maamiltoota Itoophiyaan alaa jiraniif amma hojiirra oolaa hin jiru. Hir'ina mudateef dhiifama isin gaafanna.",
        'slip_received': "Galatoomaa! Odeeffannoo kaffaltii keessan fudhanneerra. Bulchaan keenya amna ni mirkaneessa. Kun yeroo muraasa fudhachuu danda'a. Kaffaltiin keessan yeroo mirkanaa'u battalumatti ergaan isin qaqqaba. Maaloo obsaan eegaa.",
        'payment_notif_admin': (
            "🔔 **Odeeffannoo Kaffaltii Haaraa!** 🔔\n\n"
            "<b>Fayyadamaa:</b> {user_mention} (ID: `{user_id}`)\n"
            "<b>Albamii:</b> {album_title}\n\n"
            "Fayyadamtootni kun odeeffannoo kaffaltii erganii jiru. Maaloo gara ergaa isaanii deemun Lakkoofsa Raawwii ykn Screenshot ilaaluun kaffaltii mirkaneessaa.\n\n"
            "➡️ Mirkaneessuuf: as tuqi `/approve {user_id} {album_key}`\n"
            "➡️ Diduuf: as tuqi `/reject {user_id}`"
        ),
        'payment_success_user': (
            "🎉 **Baga gammaddan! Kaffaltiin keessan milkaa'inaan mirkanaa'eera!** 🎉\n\n"
            "<b>{album_title}</b> waan bitattaniif hedduu isin galateeffanna. Faarfannoonni kun jireenya keessaniif eebba akka fidan ni hawwina.\n\n"
            "Liinkii **yeroo tokkoof** qofa tajaajilu kanatti fayyadamuun chaanaalii dhuunfaa keenyatti makamuu dandeessu:\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ Dhiifama, kaffaltii keessan mirkaneessuu hin dandeenye. Iyyanni keessan kufaa ta'eera. Kun dogoggoraan ta'eera jettanii yoo amantan, maaloo bulchaa keenya kallattiin karaa [@YOUR_ADMIN_USERNAME_HERE] qunnamaa.",
        'feedback_prompt': "Faarfannoonni kun isin eebbisaa akka jiran abdii qabna! Guyyoota muraasa booda, waa'ee albamichaa yaada keessan gaafachuuf ergaa isiniif ergina.",
        'feedback_request': "Akkam {user_name}! Albamii <b>{album_title}</b> jaallattan abdii qabna. Yaada ykn dhugaa ba'umsa keessan yoo nuuf hirtan baay'ee gammana. Jechi keessan onnachiisa guddaadha!",
    },

    # ====================================================================================
    # Saho Translations (Placeholder - Uses Tigrinya)
    # ====================================================================================
    'saho': {
        'welcome_language': "ሰላም <b>{user_name}</b>! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ንኽትቅጽል ቋንቋ ምረጽ፦",
        'main_menu': (
            "እንኳዕ ብደሓን ናብ ወግዓዊ ዲጂታል መሸጢ ናይ ኣልበማት\n"
            "<b>'መዘምራን ልደታ ማርያም ቁምስና መቐለ'</b> በጻሕካ።\n\n"
            "በጃኻ ክትዕድግ እትደሊ ኣልበም ምረጽ፦"
        ),
        'album_vol_4': "እየሱስ (Vol. 4) - 300 ብር",
        'album_vol_3': "ንዓኻ ኣሚና (Vol. 3) - 100 ብር",
        'album_vol_2': "ተስፋ ኣሎና (Vol. 2) - 100 ብር",
        'album_vol_1': "ክዝምረልካ (Vol. 1) - 100 ብር",
        'how_to_buy_button': "📖 ኣገባብ ኣተዓዳድጋ",
        'back_to_main_menu_button': "⬅️ ናብ ዝርዝር ኣልበማት ተመለስ",
        'home_button': "🏠 ናብ ቀንዲ ገጽ",
        'help_button': "❔ ሓገዝ",
        'ask_payment_method': "በጃኻ ናይ ክፍያ መረጋገጺ ኣገባብካ ምረጽ።\nነቲ **Transaction ID** ከም ጽሑፍ፡ ወይ ነቲ **ናይ ክፍያ ደረሰኝ (Screenshot)** ከም ስእሊ ስደድ።",
        'payment_instructions': (
            "ብሉጽ ምርጫ! ንስኻ <b>{album_title}</b> ብ<b>{album_price} ብር</b> ትዕድግ ኣለኻ።\n\n"
            "ክፍሊት ንምፍጻም በዞም ዝስዕቡ ኣገባባት ተጠቐም፦\n\n"
            "<b><u>1. ንግዲ ባንክ ኢትዮጵያ (CBE):</u></b>\n"
            "<b>ስም:</b> [YOUR_CBE_ACCOUNT_NAME_HERE]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [YOUR_CBE_ACCOUNT_NUMBER_HERE]\n\n"
            "<b><u>2. ባንኪ ኣቢሲንያ (BOA):</u></b>\n"
            "<b>ስም:</b> [YOUR_BOA_ACCOUNT_NAME_HERE]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [YOUR_BOA_ACCOUNT_NUMBER_HERE]\n\n"
            "⚠️ <b>ኣዝዩ ኣገዳሲ:</b>\n"
            "ክፍሊትካ ምስ ፈጸምካ፡ ናብዚ ተመሊስካ ነቲ **Transaction ID** (ንኣብነት፡ `ET123...`) ወይ ነቲ **Screenshot** ክትሰደልና ኣለካ።"
        ),
        'location_out_unavailable': "ንደንበኛታትና ኣብ ወጻኢ ዚኸውን ኣገልግሎት ኣብዚ እዋን'ዚ ኣብ ስራሕ ይርከብ። ንዘጋጠመ ምድንጓይ ይቕሬታ ንሓትት።",
        'help_text_main': "<b>መርሒ:</b> እዚ ቀንዲ ገጽ እዩ። ዝኾነ ኣልበም መሪጽካ ናይ ምዕዳግ መስርሕ ክትጅምር ትኽእል ኢኻ። ዝርዝር መምርሒ እንተደሊኻ፡ 'ኣገባብ ኣተዓዳድጋ' ዝብል ቁልፊ ጠውቕ።",
        'help_text_payment': "<b>መርሒ:</b> ኣብዚ ገጽ'ዚ፡ በቶም ዝተዋህቡ ናይ ባንክ ሓበሬታታት ተጠቒምካ ክፍሊትካ ፈጽም። ድሕሪኡ፡ ነቲ Transaction ID (כמו ጽሑፍ) ወይ ነቲ ደረሰኝ (כמו ስእሊ) ናብዚ ቦት'ዚ ክትሰዶ ኣለካ።",
        'slip_received': "የቐንየልና! ናይ ክፍያ ሓበሬታኻ ተቐቢልና ኣለና። ሓደ ኣካያዲ ሕጂ ከረጋግጾ እዩ። እዚ ቁሩብ ግዜ ክወስድ ይኽእል እዩ። ምስ ተረጋገጸ ብኡንብኡ መልእኽቲ ክንሰደልካ ኢና። በጃኻ ብትዕግስቲ ጽናሕ።",
        'payment_notif_admin': (
            "🔔 **ሓድሽ ናይ ክፍያ ሓበሬታ!** 🔔\n\n"
            "<b>ተጠቃሚ:</b> {user_mention} (ID: `{user_id}`)\n"
            "<b>ኣልበም:</b> {album_title}\n\n"
            "እዚ ተጠቃሚ'ዚ ናይ ክፍያ ሓበሬታ ሰዲዱ ኣሎ። በጃኻ ናብ ውልቃዊ መልእኽቱ ኬድካ ነቲ Transaction ID ወይ Screenshot ርኢኻ ኣረጋግጽ።\n\n"
            "➡️ ንምርግጋጽ: ኣብዚ ጠውቕ `/approve {user_id} {album_key}`\n"
            "➡️ ንምንጻግ: ኣብዚ ጠውቕ `/reject {user_id}`"
        ),
        'payment_success_user': (
            "🎉 **እንኳዕ ደስ በለካ! ክፍሊትካ ብዓወት ተረጋጊጹ እዩ!** 🎉\n\n"
            "ን <b>{album_title}</b> ስለ ዝዓደግካ ኣዚና ነምስግን። እዞም መዝሙራት በረኸት ከምጽኡልካ ንምነ።\n\n"
            "ነዚ **ሓደ ግዜ ጥራይ** ዝሰርሕ መላግቦ ጠዊቕካ ናብቲ ውሑስ ቻነል ክትጽንበር ትኽእል ኢኻ፦\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቕሬታ፡ ነቲ ዝሰደድካዮ ናይ ክፍያ ሓበሬታ ከነረጋግጽ ኣይከኣልናን። ሕቶኻ ተነጺጉ ኣሎ። እዚ ብጌጋ ዝተፈጸመ ይመስለካ እንተኾይኑ፡ በጃኻ ምስ ኣካያዲና ብቐጥታ ኣብ [@YOUR_ADMIN_USERNAME_HERE] ተራኸብ።",
        'feedback_prompt': "እቶም መዝሙራት የበርኹኹም ከም ዘለዉ ተስፋ ንገብር! ድሕሪ ገለ መዓልታት፡ ሓሳብ ርኢቶኹም ንምሕታት መልእኽቲ ክንሰደልኩም ኢና።",
        'feedback_request': "ሰላም {user_name}! ነቲ ናይ <b>{album_title}</b> ኣልበም ከም እትሰምዖ ዘለኻ ተስፋ ንገብር። ሓሳብካ ወይ ምስክርነትካ እንተተካፍለና፡ ኣዚና ምተሓጎስና። ቃልካ ዓቢ መተባብዒ እዩ!",
    },
}