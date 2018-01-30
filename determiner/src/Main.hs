{-# LANGUAGE DeriveGeneric     #-}
{-# LANGUAGE OverloadedStrings #-}

module Main where

import Data.Monoid ((<>))
import Data.Aeson
import GHC.Generics
import Web.Scotty as WS
import Data.Maybe
import Network.HTTP.Client
import Control.Monad.IO.Class (liftIO)
import Network.HTTP.Simple (setRequestBodyJSON)
import Data.Map as M
import Data.List as L
import Data.Text (pack)

handStrength = fromList([("high_card",1), 
                         ("pair",2),
                         ("two_pairs",3),
                         ("three_of_a_kind",4),
                         ("straight",5),
                         ("flush",6),
                         ("full_house",7),
                         ("poker",8),
                         ("straight_flush",9),
                         ("royal_flush",10)])

data River = River { player :: String, cards :: [String] } deriving (Generic, Show)
instance ToJSON River where
    toEncoding = genericToEncoding defaultOptions

instance FromJSON River where
    parseJSON = withObject "River" $ \v -> River
        <$> v .: "player"
        <*> v .: "cards"

data Hand = Hand { value :: Integer, kind :: String, hand :: [String] } deriving (Generic, Show)
instance ToJSON Hand where
    -- this generates a Value
    toJSON (Hand value kind hand) =
        object ["kind" .= kind, "hand" .= hand]

    -- this encodes directly to a bytestring Builder
    toEncoding (Hand value kind hand) =
        pairs ("kind" .= kind <> "hand" .= hand)

instance FromJSON Hand where
    parseJSON = withObject "Hand" $ \v -> Hand
        <$> v .: "value"
        <*> v .: "kind"
        <*> v .: "hand"

instance Eq Hand where
    (Hand v1 k1 h1) == (Hand v2 k2 h2) = k1 == k2 && v1 == v2

instance Ord Hand where
    a <= b = comp a b

comp :: Hand -> Hand -> Bool
comp h1 h2 =
    if (M.lookup (kind h1) handStrength < M.lookup (kind h2) handStrength) then True
    else if (M.lookup (kind h1) handStrength == M.lookup (kind h2) handStrength) then 
        if (value h1) < (value h2) then True else False
    else False

data Res = Res { user :: String, h :: Hand } deriving (Generic, Show)
instance ToJSON Res where
    -- this generates a Value
    toJSON (Res user h) =
        object [(pack user) .= h]

instance Eq Res where
    (Res u1 h1) == (Res u2 h2) = h1 == h2

instance Ord Res where
    (Res u1 h1) <= (Res u2 h2) = comp h1 h2

send :: River -> IO Res
send x = do
    manager <- newManager defaultManagerSettings
    let request = setRequestBodyJSON (toJSON (cards x)) $ "POST http://localhost:3000/recognize"
    response <- httpLbs request manager
    let hands = decode (responseBody response) :: Maybe [Hand]
    return (Res { user = (player x), h = (maximum (fromJust hands)) })  

main = do
  putStrLn "Starting Server..."

  scotty 3010 $ do

    WS.post "/hands" $ do
        b <- body
        let river = decode b :: Maybe [River]
        let maxHands = L.map send (fromJust river)
        usersMax <- liftIO (sequence maxHands) -- sequence is used to move IO monad at first layer

        let a = (L.filter (== (maximum usersMax)) usersMax)
        WS.json a