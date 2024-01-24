import pygame as pg
import sys
import random

class Card:
    def __init__(self, x, y, width, height, text, effect_amount):
        # カードの基本情報を保持するクラス
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.effect_amount = effect_amount
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        # 画像読み込み
        self.me = pg.image.load("images/dc_pic1.png")
        self.me = pg.transform.scale(self.me, (150, 150))
        self.title = pg.image.load("images/title.png")
        self.title = pg.transform.scale(self.title,(700,400))
        self.clear = pg.image.load("images/clear.png")
        self.clear = pg.transform.scale(self.clear,(800,600))
        self.gameover = pg.image.load("images/gameover.png")
        self.gameover = pg.transform.scale(self.gameover,(800,600))
        self.friend1 = pg.image.load("images/star1.png")
        self.friend1 = pg.transform.scale(self.friend1,(150,200))
        self.friend2 = pg.image.load("images/star2.png")
        self.friend2 = pg.transform.scale(self.friend2,(150,200))
        self.friend3 = pg.image.load("images/star3.png")
        self.friend3 = pg.transform.scale(self.friend3,(150,200))
        self.friend4 = pg.image.load("images/star4.png")
        self.friend4 = pg.transform.scale(self.friend4,(150,200))
        self.friend5 = pg.image.load("images/star5.png")
        self.friend5 = pg.transform.scale(self.friend5,(150,200))
        # 手札とデッキの初期化
        self.cards = [
            Card(150, 450, 110, 130, "ありがとう", 30),
            Card(280, 450, 110, 130, "そうだね", 0),
            Card(410, 450, 110, 130, "うるさい", -20),
            Card(540, 450, 110, 130, "退屈", -10),
            Card(670, 450, 105, 130, "上手い", 10),
        ]
        self.deck = [
            Card(0, 0, 80, 110, "好き", 20),
            Card(0, 0, 80, 110, "大好き", 20),
            Card(0, 0, 80, 110, "かっこいい", 20),
            Card(0, 0, 80, 110, "可愛い", 20),
            Card(0, 0, 80, 110, "頑張って", 20),
            Card(0, 0, 80, 110, "無理しないで", 10),
            Card(0, 0, 80, 110, "大丈夫", 10),
            Card(0, 0, 80, 110, "ドンマイ", 10),
            Card(0, 0, 80, 110, "あなたのおかげ", 20),
            Card(0, 0, 80, 110, "素敵", 20),
            Card(0, 0, 80, 110, "優しい", 20),
            Card(0, 0, 80, 110, "頼もしい", 20),
            Card(0, 0, 80, 110, "センスいい", 20),
            Card(0, 0, 80, 110, "すごい", 10),
            Card(0, 0, 80, 110, "上手い", 10),
            Card(0, 0, 80, 110, "いいね", 10),
            Card(0, 0, 80, 110, "ダルイ", -10),
            Card(0, 0, 80, 110, "ウザイ", -30),
            Card(0, 0, 80, 110, "キモい", -30),
            Card(0, 0, 80, 110, "ダサい", -20),
            Card(0, 0, 80, 110, "ふざけるな", -10),
            Card(0, 0, 80, 110, "お前", -10),
            Card(0, 0, 80, 110, "クソ", -30),
            Card(0, 0, 80, 110, "ガキ", -20),
            Card(0, 0, 80, 110, "あほ", -20),
            Card(0, 0, 80, 110, "ババア", -30),
            Card(0, 0, 80, 110, "ジジイ", -30),
            Card(0, 0, 80, 110, "うんち", -30),
            Card(0, 0, 80, 110, "黙れ", -20),
            Card(0, 0, 80, 110, "クサイ", -20),
            Card(0, 0, 80, 110, "無理", -20),
            Card(0, 0, 80, 110, "面白くない", -10),
            Card(0, 0, 80, 110, "近寄るな", -10),
            Card(0, 0, 80, 110, "こんにちは", 0),
            Card(0, 0, 80, 110, "たしかに", 0),
            Card(0, 0, 80, 110, "うんうん", 0),
            Card(0, 0, 80, 110, "なるほど", 0),
        ]
        # 手札の初期化
        self.hand = random.sample(self.deck, min(len(self.cards), len(self.deck)))
        # 画面外の壁の設定
        self.walls = [
            pg.Rect(0, 0, 800, 20),
            pg.Rect(0, 0, 20, 600),
            pg.Rect(780, 0, 20, 600),
            pg.Rect(0, 580, 800, 20)
        ]
        # 画面の大きさ
        self.width = 800
        self.height = 600
        # レベル初期値
        self.level = 1
        # ターン数の初期値
        self.turns_left = 15 
        # ゲームオーバーフラグ
        self.game_over = False 
        # カードボタンを一度クリックしたかどうかのフラグ
        self.pushFlag = False
        # 相手の属性
        self.opponent_life = 50
        # サウンドの読み込み
        self.heal_sound = pg.mixer.Sound("sounds/heal.wav")
        self.attack_sound = pg.mixer.Sound("sounds/damage.wav")
        self.normal_sound = pg.mixer.Sound("sounds/pi.wav")
        # スタートボタン
        self.start_button_font = pg.font.Font("ipaexm.ttf", 36)
        self.game_started = False

    def update_game_progress(self):
        # ゲームオーバー判定
        if self.opponent_life <= 0 or self.turns_left == 0:
            self.screen.blit(self.gameover, (0, 0))
            return

        # クリア判定
        if self.opponent_life >= 100 and self.turns_left > 0:
            if self.level == 1:
                # レベル1クリア時の処理
                self.reset_game(2,10)
                # ここにレベルアップ時の初期化処理を追加する

            elif self.level == 2:
                # レベル2クリア時の処理
                self.level = 3
                self.reset_game(3,5)

            elif self.level == 3:
                self.screen.blit(self.clear, (0, 0))
                # ここにレベルアップ時の初期化処理を追加する

    def exchange_all_cards(self):
        # 手札とデッキのランダムな5枚のカードを交換するメソッド
        if self.hand and not self.pushFlag:
            # ボタンが押されたことをフラグで記録
            self.pushFlag = True

            # 手札のカードをデッキに戻す
            self.deck.extend(self.hand)
            # 手札をクリア
            self.hand.clear()
            # デッキをシャッフル
            random.shuffle(self.deck)
            # 新しい手札をランダムに選ぶ
            self.hand = random.sample(self.deck, min(len(self.cards), len(self.deck)))
            # 選ばれた手札をデッキから削除
            for card in self.hand:
                self.deck.remove(card)

            # 手札のカードをデッキの中からランダムに5枚選んで交換
            for i, card in enumerate(self.cards):
                new_card = random.choice(self.deck)
                card.text, card.effect_amount = new_card.text, new_card.effect_amount
                self.deck.remove(new_card)

    def swap_card(self, index):
        if self.hand:
            # 手札の選択されたカードとデッキのランダムなカードを交換する
            selected_card = self.cards[index]
            selected_card.text, selected_card.effect_amount = self.hand[0].text, self.hand[0].effect_amount
            # 手札のカードをデッキの最後に追加
            self.deck.append(self.hand.pop(0))
            # デッキをシャッフル
            random.shuffle(self.deck)
            # 手札からデッキにカードを入れ替えた後、新しい手札をランダムに選ぶ
            self.hand.append(random.choice(self.deck))
            # デッキから選ばれたカードを削除
            self.deck.remove(self.hand[-1])
            if self.opponent_life <= 0 or self.opponent_life >= 100:
                self.hand = []
        if self.opponent_life <= 0 or self.opponent_life >= 100:
            if self.opponent_life >= 100:
                self.FinishScreen("クリア")
            else:
                self.FinishScreen("ゲームオーバー")
                self.level = 1
                self.turns_left = 15

    #終了画面
    def FinishScreen(self, text):
        self.screen.fill(pg.Color("WHITE"))
        font = pg.font.Font("ipaexm.ttf", 50)
        finish_text = font.render(text, True, pg.Color("BLACK"))
        text_rect = finish_text.get_rect(center=(self.width / 2, self.height / 2)) 
        self.screen.blit(finish_text, text_rect)
    
        if text == "ゲームオーバー" and (self.hand == [] or self.turns_left == 0):
            restart_text = self.start_button_font.render("Rを押して戻る", True, pg.Color("BLACK"))
            text_rect = restart_text.get_rect(center=(self.width / 2, self.height / 2 + 50))
            self.screen.blit(restart_text, text_rect)


    def reset_game(self,new_level,new_life):
        # ゲームをリセットする処理
        self.opponent_life = 50
        self.level = new_level
        self.turns_left = new_life
        self.cards = [
            Card(150, 450, 110, 130, "ありがとう", 30),
            Card(280, 450, 110, 130, "そうだね", 0),
            Card(410, 450, 110, 130, "うるさい", -20),
            Card(540, 450, 110, 130, "退屈", -10),
            Card(670, 450, 110, 130, "上手い", 10),
        ]
        self.deck = [
            Card(0, 0, 80, 110, "好き", 20),
            Card(0, 0, 80, 110, "大好き", 20),
            Card(0, 0, 80, 110, "かっこいい", 20),
            Card(0, 0, 80, 110, "可愛い", 20),
            Card(0, 0, 80, 110, "頑張って", 20),
            Card(0, 0, 80, 110, "無理しないで", 10),
            Card(0, 0, 80, 110, "大丈夫", 10),
            Card(0, 0, 80, 110, "ドンマイ", 10),
            Card(0, 0, 80, 110, "あなたのおかげ", 20),
            Card(0, 0, 80, 110, "素敵", 20),
            Card(0, 0, 80, 110, "優しい", 20),
            Card(0, 0, 80, 110, "頼もしい", 20),
            Card(0, 0, 80, 110, "センスいい", 20),
            Card(0, 0, 80, 110, "すごい", 10),
            Card(0, 0, 80, 110, "上手い", 10),
            Card(0, 0, 80, 110, "いいね", 10),
            Card(0, 0, 80, 110, "ダルイ", -10),
            Card(0, 0, 80, 110, "ウザイ", -30),
            Card(0, 0, 80, 110, "キモい", -30),
            Card(0, 0, 80, 110, "ダサい", -20),
            Card(0, 0, 80, 110, "ふざけるな", -10),
            Card(0, 0, 80, 110, "お前", -10),
            Card(0, 0, 80, 110, "クソ", -30),
            Card(0, 0, 80, 110, "ガキ", -20),
            Card(0, 0, 80, 110, "あほ", -20),
            Card(0, 0, 80, 110, "ババア", -30),
            Card(0, 0, 80, 110, "ジジイ", -30),
            Card(0, 0, 80, 110, "うんち", -30),
            Card(0, 0, 80, 110, "黙れ", -20),
            Card(0, 0, 80, 110, "クサイ", -20),
            Card(0, 0, 80, 110, "無理", -20),
            Card(0, 0, 80, 110, "面白くない", -10),
            Card(0, 0, 80, 110, "近寄るな", -10),
            Card(0, 0, 80, 110, "こんにちは", 0),
            Card(0, 0, 80, 110, "たしかに", 0),
            Card(0, 0, 80, 110, "うんうん", 0),
            Card(0, 0, 80, 110, "なるほど", 0),
        ]
        # 手札のカードをデッキに戻す
        self.deck.extend(self.hand)
        # 手札をクリア
        self.hand.clear()
        # デッキをシャッフル
        random.shuffle(self.deck)
        # 新しい手札をランダムに選ぶ
        self.hand = random.sample(self.deck, min(len(self.cards), len(self.deck)))
        # 選ばれた手札をデッキから削除
        for card in self.hand:
            self.deck.remove(card)

        # 手札のカードをデッキの中からランダムに5枚選んで交換
        for i, card in enumerate(self.cards):
            new_card = random.choice(self.deck)
            card.text, card.effect_amount = new_card.text, new_card.effect_amount
            self.deck.remove(new_card)
        self.game_started = False
        
    def button_judge(self):
        mdown = pg.mouse.get_pressed()
        (mx, my) = pg.mouse.get_pos()
        if mdown[0]:
            for i, card in enumerate(self.cards):
                if card.rect.collidepoint(mx, my) and not self.pushFlag:
                    self.pushFlag = True
                    # カードの種類に応じて対応するアクションを実行
                    if card.effect_amount > 0:
                        self.opponent_life = min(100, self.opponent_life + card.effect_amount)
                        self.heal_sound.play()
                    elif card.effect_amount < 0:
                        self.opponent_life = max(0, self.opponent_life + card.effect_amount)
                        self.attack_sound.play()
                    else:
                        self.normal_sound.play()

                    # 残りゲーム数を減少させる
                    self.turns_left -= 1

                    # 使用したカードをデッキのランダムなカードと交換
                    self.swap_card(i)
        else:
            self.pushFlag = False
            
    def draw_text_on_card(self, surface, text, rect):
        # カード上にテキストを描画するメソッド
        font = pg.font.Font("ipaexm.ttf", 20)
        text_surface = font.render(text, True, pg.Color("WHITE"))
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def draw_level(self):
        font = pg.font.Font("ipaexm.ttf", 20)
        level_text = font.render(f"レベル: {self.level}", True, pg.Color("BLACK"))
        self.screen.blit(level_text, (20, 60))

    def draw_remaining_turns(self):
        font = pg.font.Font("ipaexm.ttf", 20)
        turns_text = font.render(f"残りターン: {self.turns_left}", True, pg.Color("BLACK"))
        self.screen.blit(turns_text, (20, 100))

    def draw_start_button(self):
        if self.level == 1:
            self.screen.blit(self.title,(30,30))
            start_text = self.start_button_font.render("ゲームスタート", True, pg.Color("BLACK"))
        elif self.level == 2:
            start_text = self.start_button_font.render("レベル2 スタート", True, pg.Color("BLACK"))
        elif self.level == 3:
            start_text = self.start_button_font.render("レベル3 スタート", True, pg.Color("BLACK"))
        start_rect = start_text.get_rect(center=(400, 400))
        button_rect = start_rect.inflate(10, 10)
        pg.draw.rect(self.screen, pg.Color("BLACK"), button_rect, 2)
        self.screen.blit(start_text, start_rect)
        (mx, my) = pg.mouse.get_pos()
        mdown = pg.mouse.get_pressed()
        if mdown[0]:
            if button_rect.collidepoint(mx, my):
                self.start_game()

    def draw_exchange_button(self):
        # 交換ボタンを描画
        if self.opponent_life <= 0 or self.opponent_life >= 100:
            return
        exchange_text = self.start_button_font.render("手札を交換", True, pg.Color("BLACK"))
        exchange_rect = exchange_text.get_rect(center=(650, 420))
        button_rect = exchange_rect.inflate(10, 10)
        pg.draw.rect(self.screen, pg.Color("BLACK"), button_rect, 2)
        self.screen.blit(exchange_text, exchange_rect)
        (mx, my) = pg.mouse.get_pos()
        mdown = pg.mouse.get_pressed()
        if mdown[0]:
            if button_rect.collidepoint(mx, my):
                # 交換ボタンがクリックされたら手札とデッキのカードを全て交換
                self.exchange_all_cards()

    def start_game(self):
        self.game_started = True
        self.exchange_all_cards()

    def gamestage(self):
        if self.opponent_life <= 0 or self.opponent_life >= 100:
            return
        # ゲーム画面の描画
        self.screen.fill(pg.Color("WHITE"))
        if self.game_started:
            self.screen.blit(self.me, (15, 450))
        # 画面外の壁の描画
        for wall in self.walls:
            pg.draw.rect(self.screen, pg.Color("DARKGREEN"), wall)
        if self.game_started:
            # 手札の描画
            for i, card in enumerate(self.cards):
                pg.draw.rect(self.screen, pg.Color("BLUE"), card.rect)
                self.draw_text_on_card(self.screen, card.text, card.rect)
            # カードボタンの判定
            self.button_judge()
            # 相手の体力の表示
            pg.font.init()
            font = pg.font.Font("ipaexm.ttf", 20)
            if self.hand:
                opponent_life_text = font.render(f"体力:", True, pg.Color("BLACK"))
            if self.opponent_life <= 0 or self.opponent_life >= 100:  
                opponent_life_text = font.render(f"", True, pg.Color("BLACK"))
            self.screen.blit(opponent_life_text, (20, 20))
            pg.draw.rect(self.screen, (0,0,0), (75,20,511,26))
            pg.draw.rect(self.screen, (255,255,255), (80,23,500,20))
            pg.draw.rect(self.screen, (255,0,0), (80,23,self.opponent_life*5,20))

            #友達の表示
            if(self.opponent_life>0 and self.opponent_life<=20):
                self.screen.blit(self.friend1,(600,50))
            elif(self.opponent_life>20 and self.opponent_life<=40):
                self.screen.blit(self.friend2,(600,50))
            elif(self.opponent_life>40 and self.opponent_life<=60):
                self.screen.blit(self.friend3,(600,50))
            elif(self.opponent_life>60 and self.opponent_life <= 80):
                self.screen.blit(self.friend4,(600,50))
            elif(self.opponent_life>80 and self.opponent_life<=100):
                self.screen.blit(self.friend5,(600,50))
            # レベルの表示
            self.draw_level()
            # 残りゲーム数の表示
            self.draw_remaining_turns()
            # 交換ボタンの描画
            self.draw_exchange_button()
        else:
            self.draw_start_button()

    def run(self):
        while True:
            self.gamestage()
            self.update_game_progress()  # ゲームの進行状況を更新
            pg.display.update()
            self.clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        if self.hand == [] or self.turns_left == 0 or self.opponent_life <= 0:
                            self.reset_game(1,15)

if __name__ == "__main__":
    game = Game()
    game.run()