#Сообщения для бота, которые можно легко настроить
#К каждому сообщению идет описание
#ВАЖНО! parse_mode='Markdown'

#Импорт основного файла для получения ID пользователя и реферала
#Настройка БД

chanel_username = "@SMILEETON"

#При отправке любого сообщения не соотв.условию в обработчике сообщения
ERROR_message = ('❌ Неизвестная команда!\n\n_Вы отправили сообщение напрямую в чат бота, или структура меню была изменена Админом._\n\nℹ️ Не отправляйте прямых сообщений боту или обновите Меню, нажав /start')

#Приветственное сообщение
WELCOME_message = (f'Чтобы участвовать в AIRDROP, Вам необходимо сначала подписаться на канал: {chanel_username}')

#Главное меню
MENU_message = (f'*AIRDROP SMILE COIN*\n\n*200 $SMILE* - за одного приведенного друга ? \n😱Это самые лучшие условия для масштабного AIRDOP !\n\nНичего проще не бывает! Абсолютно каждый участник получит *DROP* от *SMILE* Жми на кнопу «условия», там все подробности! Вперед!\n\n{chanel_username}')

#Условия
Terms_message = (f'*УСЛОВИЯ \\ TERMS 📃*\n\nУсловия участия в AIRDROP не были еще такими простыми 😱\nАбсолютно каждый участник получит токены $SMILE 🔥\nЧтобы участвовать, Вам необходимо:\n1. Быть подписанным на канал: {chanel_username}\n2. Пригласить всех друзей\n\nЗа каждого приведённого друга, вы получите *200* $SMILE\n\n\nВы можете приглашать друзей по вашей персональной реферальной ссылке: Here Referal LINK\n\n_пригласить/invite👇🏼_')


#Кошелек
Wallet_message = ('*Ваш кошелек:*\n\nВам нужно привязать НЕкастодиальный кошелек сети TON -\nРекомендуем - _Tonkeeper\\Tonhub\\MyTonWallet_')

#Twitter
Twitter_message = ('Вкладка не привязана к Twitter!\nОбратитесь за привязкой!')

#TERMS ENGLISH
TermsENG_message = (f'The conditions of participation in AIRDROP have never been so simple\n😱Absolutely every participant will receive $SMILE tokens 🔥\n\nTo participate, you need to:\n1. be subscribed to the channel: {chanel_username}\n2. Invite all your friends\n\nFor each friend you refer, you will receive 200 $SMILE\\n\nYou can invite friends via your personal referral link: Link\n\n_invite👇🏼_')