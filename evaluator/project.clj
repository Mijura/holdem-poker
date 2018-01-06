(defproject evaluator "0.1.0-SNAPSHOT"
      :description "REST service for documents"
      :url "http://blog.interlinked.org"
      :dependencies [[org.clojure/clojure "1.7.0"]
                     [org.clojure/math.combinatorics "0.1.3"]
                     [compojure "1.1.1"]
                     [ring/ring-json "0.4.0"]
                     [cheshire "4.0.3"]]
      :plugins [[lein-ring "0.7.3"]]
      :ring {:handler evaluator.handler/app}
      :profiles
      {:dev {:dependencies [[ring-mock "0.1.3"]]}})