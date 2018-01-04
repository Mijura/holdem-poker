(ns evaluator.handler
      (:use compojure.core)
      (:use cheshire.core)
      (:use ring.util.response)
      (:require [compojure.handler :as handler]
                [ring.middleware.json :as middleware]
                [compojure.route :as route]
                [clojure.math.combinatorics :as combo]))

(def hand-strength {:high-card 0 
                    :pair 1 
                    :two-pairs 2 
                    :three-of-a-kind 3 
                    :straight 4 
                    :flush 5 
                    :full-house 6 
                    :poker 7 
                    :straight-flush 8 
                    :royal-flush 9})

(def card-strength {:2 1 
                    :3 2 
                    :4 3 
                    :5 4 
                    :6 5 
                    :7 6 
                    :8 7 
                    :9 8 
                    :10 9 
                    :J 10 
                    :Q 11 
                    :K 12 
                    :A 13})

(defn shift-left-or [x]
  (bit-or 2r1 (bit-shift-left x 1))) 

(defn update-vals [m ks & args]
  (reduce #(apply update % %2 args) m ks))

(defn remove-last [str]
  (.substring (java.lang.String. str) 0 (- (count str) 1)))

(defn get-last [str]
  (.substring (java.lang.String. str) (- (count str) 1)))

(defn create-poker-histogram [numerics]
  (def hist (zipmap numerics (repeat 2r0)))
  (update-vals hist numerics shift-left-or))

(defn calc-val [hist]
  (reduce + (vals hist)))

(defn lazy-contains? [col key]
  (not (nil? (some #{key} col))))

(defn get-card-strength [card]
  (get card-strength (keyword (remove-last card))))

(defn get-numerics [hand]
  (map get-card-strength hand))

(defn get-suits [hand]
  (map get-last hand))

(defn exp [x n]
  (reduce * (repeat n x)))

(defn is-straight [numerics]
  (def sum (reduce + numerics))
  (def min_el (apply min numerics))
  (def max_el (apply max numerics))
  (def straight_value (+ (- (/ (* max_el (+ max_el 1)) 2) (/ (* min_el (+ min_el 1)) 2)) min_el))
  (= sum straight_value))

(defn is-lowest-straight [numerics]
  (and (lazy-contains? numerics 13)(lazy-contains? numerics 1)(lazy-contains? numerics 2)
       (lazy-contains? numerics 3)(lazy-contains? numerics 4)))

(defn is-highest-straight [numerics]
  (and (is-straight numerics)(= (reduce + numerics) 55)))

(defn find-key [value, hist]
  (filter (comp #{value} hist) (keys hist)))

(defn poker-value [hist]
  (+  (* (nth (find-key 15 hist) 0) 13) 
      (nth (find-key 1 hist) 0)))

(defn full-house-value [hist]
  (+  (* (nth (find-key 7 hist) 0) 13)
      (nth (find-key 3 hist) 0)))

(defn three-of-a-kind-value [hist]
  (def kickers (find-key 1 hist))
  (+  (* (nth (find-key 7 hist) 0) (exp 13 2))
      (* (apply max kickers) 13) 
      (apply min kickers)))

(defn two-pairs-value [hist]
  (def pairs (find-key 3 hist))
  (+  (* (apply max pairs) (exp 13 2))
      (* (apply min pairs) 13)
      (nth (find-key 1 hist) 0)))

(defn pair-value [hist]
  (def kickers (sort (find-key 1 hist)))
  (+  (* (nth (find-key 3 hist) 0) (exp 13 3)) 
      (* (nth kickers 2) (exp 13 2)) 
      (* (nth kickers 1) 13)
      (nth kickers 0)))

(defn different-cards-value [hist]
  (def kickers (sort (find-key 1 hist)))
  (+  (* (nth kickers 4) (exp 13 4)) 
      (* (nth kickers 3) (exp 13 3)) 
      (* (nth kickers 2) (exp 13 2))
      (* (nth kickers 1) 13)
      (nth kickers 0)))

(defn create-type-and-value [hist, numerics, suits]
  (def hist-value (calc-val hist))
  (cond
    (= hist-value 16) {:type "poker" :value (poker-value hist)} 
    (= hist-value 10) {:type "full-house" :value (full-house-value hist)}
    (= hist-value 9) {:type "three-of-a-kind" :value (three-of-a-kind-value hist)}
    (= hist-value 7) {:type "two-pairs" :value (two-pairs-value hist)} 
    (= hist-value 6) {:type "pair" :value (pair-value hist)}
    (= hist-value 5) 
      (cond (and (is-highest-straight numerics)
                  (apply = suits)) 
                      {:type "royal-flush" :value (different-cards-value hist)}
            (and (is-straight numerics)
                  (apply = suits)) 
                      {:type "straight-flush" :value (different-cards-value hist)}
            (and (is-lowest-straight numerics)
                  (apply = suits)) 
                      {:type "straight-flush" :value (different-cards-value hist)}
            (apply = suits) 
                      {:type "flush" :value (different-cards-value hist)}
            (is-straight numerics) 
                      {:type "straight" :value (different-cards-value hist)}
            (is-lowest-straight numerics) 
                      {:type "straight" :value (different-cards-value hist)}
            :else 
                      {:type "high-card" :value (different-cards-value hist)})))

(defn create-response [hand result]
  (hash-map :hand hand, 
            :hand-type (get result :type), 
            :value (get result :value)))

(defn recognize-hand [cards]
  ;creates all combinations with 5 cards
  (def hands (combo/combinations cards 5))

  ;splits card to numeric and suit
  (def numerics (map get-numerics hands))
  (def suits (map get-suits hands))

  (def poker-histogram (map create-poker-histogram numerics))
  
  (def result (map create-type-and-value poker-histogram numerics suits))
  (map create-response hands result))

(defroutes app-routes
  (POST "/recognize" {body :body} (response (recognize-hand body)))
  (route/not-found "Not Found"))

(def app
  (-> (handler/api app-routes)
      (middleware/wrap-json-body)
      (middleware/wrap-json-response)))