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

(defn create-poker-histogram [hand]
  (def numerics (for [card hand] (remove-last card)))
  (def hist (zipmap numerics (repeat 2r0)))
  (update-vals hist numerics shift-left-or))

(defn calc-val [hist]
  (reduce + (vals hist)))

(defn lazy-contains? [col key]
  (not (nil? (some #{key} col))))

(defn is-lowest-straight [numerics]
  (and (lazy-contains? numerics 13)  
       (lazy-contains? numerics 1) 
       (lazy-contains? numerics 2)
       (lazy-contains? numerics 3)
       (lazy-contains? numerics 4)))

(defn create-result [hist-value, hand]
  (def numerics (for [card hand] (get card-strength (keyword (remove-last card)))))
  (def suits (for [card hand] (get-last card)))
  (def value (reduce + numerics))

  (def min_el (apply min numerics))
  (def max_el (apply max numerics))
  (def straight_value (+ (- (/ (* max_el (+ max_el 1)) 2) (/ (* min_el (+ min_el 1)) 2)) min_el))

  (def hand-type (cond
    (= hist-value 16) "poker"
    (= hist-value 10) "full-house"
    (= hist-value 9) "three-of-a-kind"
    (= hist-value 7) "two-pairs"
    (= hist-value 6) "pair"
    (= hist-value 5) 
      (cond (and (= straight_value value) (= value 55) (apply = suits)) "royal-flush"
            (and (= straight_value value) (apply = suits)) "straight-flush"
            (and (is-lowest-straight numerics) (apply = suits)) "straight-flush"
            (apply = suits) "flush"
            (= straight_value value) "straight"
            (is-lowest-straight numerics) "straight"
            :else "high-card")))

  (def value 
    (cond (is-lowest-straight numerics) (- value 13)
          :else value))
  (hash-map :hand hand, :value value, :hand-type hand-type))

(defn recognize-hand [cards]
  (doseq [hand (combo/combinations cards 5)]
    (println (create-result (calc-val (create-poker-histogram hand)) hand))
    )(println "------------------------"))

(defroutes app-routes
  (POST "/recognize" {body :body} (recognize-hand body))
  (route/not-found "Not Found"))

(def app
  (-> (handler/api app-routes)
    (middleware/wrap-json-body)
    (middleware/wrap-json-response)))