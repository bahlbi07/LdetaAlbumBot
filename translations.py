# translations.py

# ===================================================================================
# Placeholder Guide:
# [text to be replaced] -> This is where you fill in your actual info.
# [translation needed]   -> This is where you or a translator will write the text.
# ===================================================================================

TRANSLATIONS = {
    # ================================== English ========================================
    'en': {
        'language_select_prompt': "Please choose your language:",
        'welcome_message': "Welcome <b>{user_name}</b>!\n\nThis is the official digital store for the albums of the <b>'Lideta Mariam Choir, Qumsna Mekelle'</b>.",
        'main_menu_prompt': "Please select an option below:",
        'ask_location': "Great! Please select your location to see payment options:",
        
        # --- Album Titles & Prices ---
        'album_vol_4': "🎶 Eyesus (Vol. 4) - 300 ETB",
        'album_vol_3': "🎶 Ne'aka Amina (Vol. 3) - 100 ETB",
        'album_vol_2': "🎶 Tesfa Alona (Vol. 2) - 100 ETB",
        'album_vol_1': "🎶 Kezimrelka (Vol. 1) - 100 ETB",
        
        # --- Buttons ---
        'location_in_button': "🇪🇹 Inside Ethiopia",
        'location_out_button': "🌍 Outside Ethiopia",
        'how_to_buy_button': "📖 How to Buy Guide",
        'help_button': "❔ Help",
        'home_button': "🏠 Main Menu",
        'back_button': "⬅️ Back",
        
        # --- Payment Flow ---
        'payment_instructions_ethiopia': (
            "You are purchasing <b>{album_title}</b> for <b>{album_price} ETB</b>.\n\n"
            "To complete your purchase, please use one of the payment methods below:\n\n"
            "<b><u>1. Commercial Bank of Ethiopia (CBE):</u></b>\n"
            "<b>Name:</b> [Mahber Mezamran Lodeta Maryam K.MK]\n"
            "<b>Account No:</b> [1000639550323]\n\n"
            "<b><u>2. Bank of Abyssinia (BOA):</u></b>\n"
            "<b>Name:</b> [Mahber Mezamran Lideta Maryam]\n"
            "<b>Account No:</b> [196302506]\n\n"
            "⚠️ <b><u>Next Step (Very Important):</u></b>\n"
            "After paying, you must send your payment proof to this bot.\n\n"
            "➡️ Send the **Transaction ID** (e.g., ET123...) as a text message.\n"
            "OR\n"
            "➡️ Send the payment **Screenshot** as a photo."
        ),
        'location_out_unavailable': "We are currently setting up international payment systems. This option will be available very soon. We apologize for the inconvenience.",
        'proof_received': "Thank you! We have received your payment information. An admin will verify it shortly. You will receive a notification as soon as it is approved. Please be patient.",
        
        # --- Help & Guide Texts ---
        'guide_text': "[English translation needed for the detailed 'How to Buy' guide. Explain the steps: 1. Select Language, 2. Select Album, 3. Select Location, 4. Make Payment, 5. Send Proof (ID or Screenshot), 6. Wait for Approval.]",
        'help_text_main_menu': "[English translation needed for Help on the main menu page. Explain what each album button does and the purpose of the 'How to Buy' guide.]",
        'help_text_location': "[English translation needed for Help on the location selection page. Explain why location is needed (different payment options).]",
        'help_text_payment': "[English translation needed for Help on the payment page. Re-emphasize the importance of sending the Transaction ID or Screenshot correctly after payment.]",

        # --- Admin & Post-Purchase ---
        'admin_notification': (
            "🔔 **New Payment Submission!**\n\n"
            "<b>User:</b> {user_mention} (ID: `{user_id}`)\n"
            "<b>Album:</b> {album_title}\n\n"
            "Please check for their Transaction ID or Screenshot and verify the payment.\n\n"
            "➡️ To APPROVE, click: `/approve {user_id} {album_key}`\n"
            "➡️ To REJECT, click: `/reject {user_id}`"
        ),
        'approve_success_user_auto_add': "🎉 **Congratulations, {user_name}! Your payment is verified.**\n\nYou have been automatically added to the <b>{album_title}</b> channel. You can find it in your chat list. Thank you for your support!",
        'approve_success_user_privacy': (
            "🎉 **Congratulations, {user_name}! Your payment is verified.**\n\n"
            "We tried to add you to the channel automatically, but your privacy settings prevented it. No problem!\n\n"
            "Please use this **one-time** private link to join:\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ We are sorry, but there was an issue verifying your payment. Your request has been declined. If you believe this is a mistake, please contact our admin directly at [@Dmtsibereket] for assistance.",
        'feedback_prompt': "In a few days, we will send a message asking for your valuable feedback on the album.",
        'feedback_request': "Hello {user_name}! We hope you have been blessed by the <b>{album_title}</b> album. We would be grateful if you could share your feedback or testimony. Your words are a great encouragement to us!",
        'contact_admin_prompt': "If you have any questions or need direct assistance, please contact our admin: @Dmtsibereket",
    },

    # ================================== Tigrinya =======================================
    'ti': {
        'welcome_language': "ሰላም <b>{user_name}</b>! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ንኽትቅጽል ቋንቋ ምረጽ፦",
        'welcome_message': "እንኳዕ ብደሓን ናብ ወግዓዊ ዲጂታል መሸጢ ኣልበማት\n<b>'መዘምራን ልደታ ማርያም ቁምስና መቐለ'</b> በጻሕካ።",
        'main_menu_prompt': "በጃኻ ካብዞም ዝስዕቡ ሓደ ምረጽ፦",
        'ask_location': "ብሉጽ! ክፍሊት ንምፍጻም በጃኻ ኣበይ ከም ዘለኻ ምረጽ፦",

        'album_vol_4': "🎶 እየሱስ (Vol. 4) - 300 ብር",
        'album_vol_3': "🎶 ንዓኻ ኣሚና (Vol. 3) - 100 ብር",
        'album_vol_2': "🎶 ተስፋ ኣሎና (Vol. 2) - 100 ብር",
        'album_vol_1': "🎶 ክዝምረልካ (Vol. 1) - 100 ብር",

        'location_in_button': "🇪🇹 ኣብ ውሽጢ ኢትዮጵያ",
        'location_out_button': "🌍 ካብ ኢትዮጵያ ወጻኢ",
        'how_to_buy_button': "📖 ኣገባብ ኣተዓዳድጋ",
        'help_button': "❔ ሓገዝ",
        'home_button': "🏠 ናብ ቀንዲ ገጽ",
        'back_button': "⬅️ ናብ ዝሓለፈ ተመለስ",

        'payment_instructions_ethiopia': (
            "ን <b>{album_title}</b> ብ<b>{album_price} ብር</b> ትዕድግ ኣለኻ።\n\n"
            "ክፍሊት ንምፍጻም በዞም ዝስዕቡ ኣገባባት ተጠቐም፦\n\n"
            "<b><u>1. ንግዲ ባንክ ኢትዮጵያ (CBE):</u></b>\n"
            "<b>ስም:</b> [Mahber Mezamran Lodeta Maryam K.MK]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [1000639550323]\n\n"
            "<b><u>2. ባንኪ ኣቢሲንያ (BOA):</u></b>\n"
            "<b>ስም:</b> [Mahber Mezamran Lideta Maryam]\n"
            "<b>ቁጽሪ ሕሳብ:</b> [196302506]\n\n"
            "⚠️ <b><u>ዝቕጽል ስጉምቲ (ኣዝዩ ኣገዳሲ):</u></b>\n"
            "ክፍሊትካ ምስ ፈጸምካ፡ ናይ ክፍያ መረጋገጺ ናብዚ ቦት'ዚ ክትሰድድ ኣለካ።\n\n"
            "➡️ ነቲ **Transaction ID** (ንኣብነት፡ ET123...) ከም ጽሑፍ ስደድ።\n"
            "ወይ ድማ\n"
            "➡️ ነቲ ናይ ክፍያ **Screenshot** ከም ስእሊ ስደድ።"
        ),
        'location_out_unavailable': "ንደንበኛታትና ኣብ ወጻኢ ዚኸውን ኣገልግሎት ኣብዚ እዋን'ዚ ኣብ ምድላው ንርከብ። ድሕሪ ቁሩብ እዋን ክንጅምር ኢና። ንዘጋጠመ ምድንጓይ ይቕሬታ ንሓትት።",
        'guide_text': "[ብትግርኛ ዝተጻሕፈ ዝርዝር 'ኣገባብ ኣተዓዳድጋ' መምርሒ ኣብዚ ይኣቱ። ነቶም ስጉምትታት ግለጽ: 1. ቋንቋ ምረጽ, 2. ኣልበም ምረጽ, 3. ቦታኻ ምረጽ, 4. ክፍሊት ፍጸም, 5. መረጋገጺ ስደድ (ID ወይ Screenshot), 6. ንምርግጋጽ ጽናሕ።]",
        'help_text_main_menu': "[ን ቀንዲ ገጽ ዝኸውን ናይ ሓገዝ ጽሑፍ ኣብዚ ይኣቱ። ነፍሲ ወከፍ ቁልፊ ናይ ኣልበም እንታይ ከም ዝገብርን እቲ 'ኣገባብ ኣተዓዳድጋ' ንምንታይ ከም ዘገልግልን ግለጽ።]",
        'help_text_location': "[ን ናይ ቦታ ምርጫ ገጽ ዝኸውን ናይ ሓገዝ ጽሑፍ ኣብዚ ይኣቱ። ቦታ ምሕታት ስለምንታይ ከም ዘድለየ ግለጽ (ንዝተፈላለየ ኣገባብ ክፍሊት)።]",
        'help_text_payment': "[ን ናይ ክፍያ ገጽ ዝኸውን ናይ ሓገዝ ጽሑፍ ኣብዚ ይኣቱ። ድሕሪ ክፍሊት፡ Transaction ID ወይ Screenshot ብትኽክል ምስዳድ ክሳብ ክንደይ ኣገዳሲ ምዃኑ ኣጕልሕ።]",
        'slip_received': "የቐንየልና! ናይ ክፍያ ሓበሬታኻ ተቐቢልናዮ ኣለና። ሓደ ኣካያዲ ሕጂ ከረጋግጾ እዩ። እዚ ቁሩብ ግዜ ክወስድ ይኽእል እዩ። ምስ ተረጋገጸ ብኡንብኡ መልእኽቲ ክትቅበል ኢኻ። በጃኻ ብትዕግስቲ ጽናሕ።",
        'payment_success_user_auto_add': "🎉 **እንኳዕ ደስ በለካ {user_name}! ክፍሊትካ ተረጋጊጹ እዩ።**\n\nብኣውቶማቲክ ናብቲ ናይ <b>{album_title}</b> ቻነል ተጸንቢርካ ኣለኻ። ኣብ ዝርዝር ቻናላትካ ክትረኽቦ ትኽእል ኢኻ። ንደገፍካ ነመስግን!",
        'payment_success_user_privacy': (
            "🎉 **እንኳዕ ደስ በለካ {user_name}! ክፍሊትካ ተረጋጊጹ እዩ።**\n\n"
            "ብኣውቶማቲክ ከነጸንብረካ ፈቲና ነይርና፡ ግን እቲ ናይ ውልቂ ቅጥዒኻ (privacy settings) ስለ ዝኸልከለና ኣይከኣልናን። ጸገም የለን!\n\n"
            "በጃኻ ነዚ **ሓደ ግዜ ጥራይ** ዝሰርሕ ናይ ውልቂ መላግቦ ተጠቒምካ ተጸንበር፦\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቕሬታ፡ ነቲ ዝሰደድካዮ ናይ ክፍያ ሓበሬታ ከነረጋግጽ ኣይከኣልናን። ሕቶኻ ተነጺጉ ኣሎ። እዚ ብጌጋ ዝተፈጸመ ይመስለካ እንተኾይኑ፡ በጃኻ ምስ ኣካያዲና ብቐጥታ ኣብ [@Dmtsibereket] ተራኸብ።",
        'feedback_prompt': "ድሕሪ ገለ መዓልታት፡ ሓሳብ ርኢቶኹም ንምሕታት መልእኽቲ ክንሰደልኩም ኢና።",
        'feedback_request': "ሰላም {user_name}! ነቲ ናይ <b>{album_title}</b> ኣልበም ትባረኹሉ ከም ዘለኹም ተስፋ ንገብር። ሓሳብኩም ወይ ምስክርነትኩም እንተተካፍሉና፡ ንኣገልግሎትና ዓቢ መተባብዒ እዩ!",
        'contact_admin_prompt': "ዝኾነ ሕቶ እንተሃልዩካ ወይ ቀጥታዊ ሓገዝ እንተደሊኻ፡ በጃኻ ምስ ኣካያዲና ተራኸብ: @Dmtsibereket",
    },

    # ================================== Amharic ========================================
    'am': {
        'welcome_language': "ሰላም <b>{user_name}</b>! እንኳን ደህና መጡ።\n\nእባክዎ ለመቀጠל ቋንቋ ይምረጡ:",
        'welcome_message': "እንኳን ወደ <b>'የልደታ ማርያም መዘምራን ቁምስና መቀሌ'</b> ይፋዊ ዲጂታል የአልበም መሸጫ በደህና መጡ።",
        'main_menu_prompt': "እባክዎ ከታች ካሉት አማራጮች አንዱን ይምረጡ:",
        'ask_location': "በጣም ጥሩ! ክፍያ ለመፈጸም እባክዎ አሁን ያሉበትን ቦታ ይምረጡ:",
        'album_vol_4': "🎶 ኢየሱስ (Vol. 4) - 300 ብር",
        'album_vol_3': "🎶 አንተን አምና (Vol. 3) - 100 ብር",
        'album_vol_2': "🎶 ተስፋ አለን (Vol. 2) - 100 ብር",
        'album_vol_1': "🎶 ልዘምርልህ (Vol. 1) - 100 ብር",
        'location_in_button': "🇪🇹 በኢትዮጵያ ውስጥ",
        'location_out_button': "🌍 ከኢትዮጵያ ውጪ",
        'how_to_buy_button': "📖 እንዴት መግዛት ይቻላል",
        'help_button': "❔ እርዳታ",
        'home_button': "🏠 ወደ ዋናው ምናሌ",
        'back_button': "⬅️ ወደ ኋላ ተመለስ",
        'slip_sent_button': "✅ የክፍያ ማረጋገጫውን ልኬያለሁ",
        'payment_instructions_ethiopia': (
            "እርስዎ <b>{album_title}</b>ን በ<b>{album_price} ብር</b> እየገዙ ነው።\n\n"
            "ክፍያ ለመፈጸም ከሚከተሉት መንገዶች አንዱን ይጠቀሙ፦\n\n"
            "<b><u>1. የኢትዮጵያ ንግድ ባንክ (CBE):</u></b>\n"
            "<b>ስም:</b> [Mahber Mezamran Lodeta Maryam K.MK]\n"
            "<b>የሂሳብ ቁጥር:</b> [1000639550323]\n\n"
            "<b><u>2. አቢሲንያ ባንክ (BOA):</u></b>\n"
            "<b>ስም:</b> [Mahber Mezamran Lideta Maryam]\n"
            "<b>የሂሳብ ቁጥር:</b> [196302506]\n\n"
            "⚠️ <b><u>ቀጣይ እርምጃ (በጣም አስፈላጊ):</u></b>\n"
            "ክፍያ ከፈጸሙ በኋላ، የክፍያ ማረጋገጫዎን ወደዚህ ቦት መላክ አለብዎት።\n\n"
            "➡️ የ**Transaction ID** (ለምሳሌ፡ ET123...) በጽሑፍ ይላኩ።\n"
            "ወይም\n"
            "➡️ የክፍያ **Screenshot** በፎቶ ይላኩ።"
        ),
        'location_out_unavailable': "ከኢትዮጵያ ውጪ ላሉ ደንበኞች የሚሆን አገልግሎት በአሁኑ ሰዓት በዝግጅት ላይ ነው። ስለተፈጠረው መዘግየት ይቅርታ እንጠይቃለን።",
        'guide_text': "[ዝርዝር 'እንዴት መግዛት ይቻላል' መመሪያ በአማርኛ እዚህ ያስገቡ። ደረጃዎቹን ያስረዱ: 1. ቋንቋ ይምረጡ, 2. አልበም ይምረጡ, 3. ቦታዎን ይምረጡ, 4. ክፍያ ይፈጽሙ, 5. ማረጋገጫ ይላኩ (ID ወይም Screenshot), 6. ማረጋገጫ ይጠብቁ።]",
        'help_text_main_menu': "[ለዋናው ምናሌ ገጽ የእርዳታ ጽሑፍ እዚህ ያስገቡ። እያንዳንዱ የአልበም ቁልፍ ምን እንደሚሰራ እና 'እንዴት መግዛት ይቻላል' የሚለው መመሪያ ለምን እንደሚያገለግል ያስረዱ።]",
        'help_text_location': "[ለቦታ ምርጫ ገጽ የእርዳታ ጽሑፍ እዚህ ያስገቡ። ቦታ ለምን እንደሚያስፈልግ ያስረዱ (ለተለያዩ የክፍያ አማራጮች)።]",
        'help_text_payment': "[ለክፍያ ገጽ የእርዳታ ጽሑፍ እዚህ ያስገቡ። ከክፍያ በኋላ Transaction ID ወይም Screenshot በትክክል መላክ ምን ያህል አስፈላጊ እንደሆነ አጽንኦት ይስጡ።]",
        'slip_received': "እናመሰግናለን! የክፍያ መረጃዎ ደርሶናል። አንድ አስተዳዳሪ አሁን ያረጋግጣል። ይህ የተወሰነ ጊዜ ሊወስድ ይችላል። ማረጋገጫ ሲያገኝ ወዲያውኑ መልእክት ይደርስዎታል። እባክዎ በትዕግስት ይጠብቁ።",
        'payment_success_user_auto_add': "🎉 **እንኳን ደስ አለዎት {user_name}! ክፍያዎ ተረጋግጧል።**\n\nበራስ-ሰር ወደ <b>{album_title}</b> ቻናል ተጨምረዋል። በቻት ዝርዝርዎ ውስጥ ሊያገኙት ይችላሉ። ለድጋፍዎ እናመሰግናለን!",
        'payment_success_user_privacy': (
            "🎉 **እንኳን ደስ አለዎት {user_name}! ክፍያዎ ተረጋግጧል።**\n\n"
            "በራስ-ሰር ልንጨምርዎት ሞክረን ነበር፣ ነገር ግን የእርስዎ የግላዊነት ቅንብር ከልክሎናል። ችግር የለም!\n\n"
            "እባክዎ ይህንን **የአንድ ጊዜ** የግል ሊንክ ተጠቅመው ይቀላቀሉ፦\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ ይቅርታ፣ የላኩትን የክፍያ መረጃ ማረጋገጥ አልቻልንም። ጥያቄዎ ውድቅ ተደርጓል። ይህ በስህተት እንደሆነ ካመኑ፣ እባክዎ አስተዳዳሪያችንን በቀጥታ በ [@Dmtsibereket] ያግኙ።",
        'feedback_prompt': "ከጥቂት ቀናት በኋላ፣ ስለ አልበሙ ያለዎትን አስተያየት ለመጠየቅ መልእክት እንልክልዎታለን።",
        'feedback_request': "ሰላም {user_name}! የ<b>{album_title}</b>ን አልበም እንደወደዱት ተስፋ እናደርጋለን። አስተያየትዎን ወይም ምስክርነትዎን ቢያካፍሉን በጣም እንደሰታለን። ቃልዎ ትልቅ ማበረታቻ ነው!",
        'contact_admin_prompt': "ማንኛውም ጥያቄ ካለዎት ወይም ቀጥተኛ እርዳታ ከፈለጉ፣ እባክዎ አስተዳዳሪያችንን ያግኙ: @Dmtsibereket",
    },

    # ================================== Afaan Oromoo =====================================
    'om': {
        'welcome_language': "Baga nagaan dhuftan <b>{user_name}</b>!\n\nMaaloo itti fufuuf afaan filadhaa:",
        'welcome_message': "Gara bot gurgurtaa albamii arfaffaa\n<b>'Garee Mezemran Lideta Mariam Qumsna Maqalee'</b>-tti nagaan dhuftan.",
        'main_menu_prompt': "Maaloo filannoowwan armaan gadii keessaa tokko filadhaa:",
        'ask_location': "Gaarii dha! Kaffaltii raawwachuuf maaloo iddoo jirtan filadhaa:",
        'album_vol_4': "🎶 Iyyasuus (Vol. 4) - 300 ETB",
        'album_vol_3': "🎶 Si Amannee (Vol. 3) - 100 ETB",
        'album_vol_2': "🎶 Abdii Qabna (Vol. 2) - 100 ETB",
        'album_vol_1': "🎶 Sin Faarsina (Vol. 1) - 100 ETB",
        'location_in_button': "🇪🇹 Itoophiyaa Keessa",
        'location_out_button': "🌍 Itoophiyaan Alatti",
        'how_to_buy_button': "📖 Akkamitti Bittam",
        'help_button': "❔ Gargaarsa",
        'home_button': "🏠 Gara Fuula Jalqabaatti",
        'back_button': "⬅️ Duubatti Deebi'i",
        'slip_sent_button': "✅ Nagahee kaffaltii ergeera",
        'payment_instructions_ethiopia': (
            "Albamii <b>{album_title}</b> gatii <b>{album_price} ETB</b>-tiin bitachaa jirtu.\n\n"
            "Kaffaltii raawwachuuf tooftaalee armaan gadii keessaa tokko fayyadamaa:\n\n"
            "<b><u>1. Baankii Daldalaa Itiyoophiyaa (CBE):</u></b>\n"
            "<b>Maqaa:</b> [Mahber Mezamran Lodeta Maryam K.MK]\n"
            "<b>Lak. Herreegaa:</b> [1000639550323]\n\n"
            "<b><u>2. Baankii Abisiiniyaa (BOA):</u></b>\n"
            "<b>Maqaa:</b> [Mahber Mezamran Lideta Maryam]\n"
            "<b>Lak. Herreegaa:</b> [196302506]\n\n"
            "⚠️ <b><u>Itti Aansuun (Hedduu Barbaachisaa):</u></b>\n"
            "Kaffaltii erga raawwattanii booda, mirkaneessa kaffaltii keessan gara bot kanaatti erguu qabdu.\n\n"
            "➡️ **Transaction ID** (fkn, ET123...) akka barruutti ergaa.\n"
            "YKN\n"
            "➡️ **Screenshot** kaffaltii akka suuraatti ergaa."
        ),
        'location_out_unavailable': "Tajaajilli maamiltoota Itoophiyaan alaa jiraniif amma qophiirra jira. Yeroo dhiyootti ni jalqabna. Tajaajilichi yeroon waan hin eegalleef dhiifama isin gaafanna.",
        'guide_text': "[Qajeelfama 'Akkamitti Bittam' guutuu Afaan Oromootiin asitti galchaa. Tarkaanfiiwwan ibsaa: 1. Afaan Filadhu, 2. Albamii Filadhu, 3. Iddoo Filadhu, 4. Kaffaltii Raawwadhu, 5. Mirkaneessa Ergi (ID ykn Screenshot), 6. Mirkaneeffama Eegi.]",
        'help_text_main_menu': "[Qajeelfama gargaarsaa fuula duraatiif asitti galchaa. Qabduuleen albamii hundi maal akka hojjetan fi faayidaa qajeelfama 'Akkamitti Bittam' ibsaa.]",
        'help_text_location': "[Qajeelfama gargaarsaa fuula filannoo iddoof asitti galchaa. Filannoon iddoo maaliif akka barbaachisu ibsaa (sababa filannoowwan kaffaltii adda addaatiif).]",
        'help_text_payment': "[Qajeelfama gargaarsaa fuula kaffaltiif asitti galchaa. Kaffaltii booda, Transaction ID ykn Screenshot sirriitti erguun hammam barbaachisaa akka ta'e irra deebi'ii ibsaa.]",
        'slip_received': "Galatoomaa! Odeeffannoon kaffaltii keessan nu ga'eera. Bulchaan keenya yeroo gabaabaa keessatti ni mirkaneessa. Yeroo mirkanaa'u battalumatti ergaan isin qaqqaba. Maaloo obsaan eegaa.",
        'payment_success_user_auto_add': "🎉 **Baga gammaddan {user_name}! Kaffaltiin keessan mirkanaa'eera.**\n\nOfiin isiniif chaanaalii <b>{album_title}</b> tti dabalamtaniittu. Tarree haasawa keessan keessatti argachuu dandeessu. Deeggarsa keessaniif galatoomaa!",
        'payment_success_user_privacy': (
            "🎉 **Baga gammaddan {user_name}! Kaffaltiin keessan mirkanaa'eera.**\n\n"
            "Ofiin isin dabaluuf yaallee turre, garuu seettiin dhuunfaa keessanii nu dhoowweera. Rakkoo hin qabu!\n\n"
            "Maaloo liinkii dhuunfaa **yeroo tokkoof** qofa hojjetu kanaan fayyadamuun nutti makamaa:\n"
            "🔗 <b>{invite_link}</b>"
        ),
        'payment_rejected_user': "❌ Dhiifama, odeeffannoo kaffaltii keessan mirkaneessuu hin dandeenye. Iyyanni keessan kufaa ta'eera. Kun dogoggoraan ta'eera jettanii yoo amantan, maaloo bulchaa keenya kallattiin karaa [@Dmtsibereket] qunnamaa.",
        'feedback_prompt': "Guyyoota muraasa booda, waa'ee albamichaa yaada keessan gaafachuuf ergaa isiniif ergina.",
        'feedback_request': "Akkam {user_name}! Albamii <b>{album_title}</b> jaallattan abdii qabna. Yaada ykn dhugaa ba'umsa keessan yoo nuuf hirtan baay'ee gammana. Jechi keessan onnachiisa guddaadha!",
        'contact_admin_prompt': "Gaaffii kamiyyuu yoo qabaattan ykn gargaarsa kallattii yoo barbaaddan, maaloo bulchaa keenya qunnamaa: @Dmtsibereket",
    },

    # ================================== Saho (using Tigrinya as placeholder) ===============================
    'saho': {
        'welcome_language': "ሰላም <b>{user_name}</b>! እንኳዕ ብደሓን መጻእካ።\n\nበጃኻ ንኽትቅጽል ቋንቋ ምረጽ፦",
        'welcome_message': "እንኳዕ ብደሓን ናብ ወግዓዊ ዲጂታል መሸጢ ናይ ኣልበማት\n<b>'መዘምራን ልደታ ማርያም ቁምስና መቐለ'</b> በጻሕካ።\n\nበጃኻ ክትዕድግ እትደሊ ኣልበም ምረጽ፦",
        'main_menu_prompt': "በጃኻ ካብዞም ዝስዕቡ ሓደ ምረጽ፦",
        'ask_location': "ብሉጽ! ክፍሊት ንምፍጻም በጃኻ ኣበይ ከም ዘለኻ ምረጽ፦",
        'album_vol_4': "🎶 እየሱስ (Vol. 4) - 300 ብር",
        'album_vol_3': "🎶 ንዓኻ ኣሚና (Vol. 3) - 100 ብር",
        'album_vol_2': "🎶 ተስፋ ኣሎና (Vol. 2) - 100 ብር",
        'album_vol_1': "🎶 ክዝምረልካ (Vol. 1) - 100 ብር",
        'location_in_button': "🇪🇹 ኣብ ውሽጢ ኢትዮጵያ",
        'location_out_button': "🌍 ካብ ኢትዮጵያ ወጻኢ",
        'how_to_buy_button': "📖 ኣገባብ ኣተዓዳድጋ",
        'help_button': "❔ ሓገዝ",
        'home_button': "🏠 ናብ ቀንዲ ገጽ",
        'back_button': "⬅️ ናብ ዝሓለፈ ተመለስ",
        'slip_sent_button': "✅ ነቲ ደረሰኝ ለኣኸዮ ኣለኹ",
        'payment_instructions_ethiopia': "[SAHO: Please translate the payment instructions. Show album_title and album_price. Provide CBE and BOA details. Explain that they need to send Transaction ID or Screenshot.]",
        'location_out_unavailable': "ንደንበኛታትና ኣብ ወጻኢ ዚኸውን ኣገልግሎት ኣብዚ እዋን'ዚ ኣብ ስራሕ ይርከብ። ንዘጋጠመ ምድንጓይ ይቕሬታ ንሓትት።",
        'guide_text': "[SAHO translation needed for 'How to Buy' guide.]",
        'help_text_main_menu': "[SAHO translation needed for main menu help.]",
        'help_text_location': "[SAHO translation needed for location help.]",
        'help_text_payment': "[SAHO translation needed for payment help.]",
        'slip_received': "የቐንየልና! ናይ ክፍያ ሓበሬታኻ ተቐቢልናዮ ኣለና። ሓደ ኣካያዲ ሕጂ ከረጋግጾ እዩ። ምስ ተረጋገጸ መልእኽቲ ክንሰደልካ ኢና።",
        'payment_success_user_auto_add': "🎉 **እንኳዕ ደስ በለካ {user_name}! ክፍሊትካ ተረጋጊጹ እዩ።**\n\nብኣውቶማቲክ ናብቲ ናይ <b>{album_title}</b> ቻነል ተጸንቢርካ ኣለኻ።",
        'payment_success_user_privacy': "🎉 **እንኳዕ ደስ በለካ {user_name}! ክፍሊትካ ተረጋጊጹ እዩ።**\n\nብኣውቶማቲክ ከነጸንብረካ ፈቲና፡ ግን እቲ ናይ ውልቂ ቅጥዒኻ ስለ ዝኸልከለና ኣይከኣልናን።\n\nበጃኻ ነዚ ሓደ ግዜ ዝሰርሕ መላግቦ ተጠቒምካ ተጸንበር፦\n🔗 <b>{invite_link}</b>",
        'payment_rejected_user': "❌ ይቕሬታ፡ ነቲ ዝሰደድካዮ ናይ ክፍያ ሓበሬታ ከነረጋግጽ ኣይከኣልናን። ሕቶኻ ተነጺጉ ኣሎ። በጃኻ ምስ ኣካያዲና ኣብ [@Dmtsibereket] ተራኸብ።",
        'feedback_prompt': "ድሕሪ ገለ መዓልታት፡ ሓሳብ ርኢቶኹም ንምሕታት መልእኽቲ ክንሰደልኩም ኢና።",
        'feedback_request': "ሰላም {user_name}! ነቲ ናይ <b>{album_title}</b> ኣልበም ትባረኹሉ ከም ዘለኹም ተስፋ ንገብር። ሓሳብኩም ወይ ምስክርነትኩም እንተተካፍሉና፡ ንኣገልግሎትና ዓቢ መተባብዒ እዩ!",
        'contact_admin_prompt': "ዝኾነ ሕቶ እንተሃልዩካ ወይ ሓገዝ እንተደሊኻ፡ ምስ ኣካያዲና ተራኸብ: @Dmtsibereket",
    },
}