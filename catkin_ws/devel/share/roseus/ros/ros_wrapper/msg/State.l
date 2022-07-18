;; Auto-generated. Do not edit!


(when (boundp 'ros_wrapper::State)
  (if (not (find-package "ROS_WRAPPER"))
    (make-package "ROS_WRAPPER"))
  (shadow 'State (find-package "ROS_WRAPPER")))
(unless (find-package "ROS_WRAPPER::STATE")
  (make-package "ROS_WRAPPER::STATE"))

(in-package "ROS")
;;//! \htmlinclude State.msg.html


(defclass ros_wrapper::State
  :super ros::object
  :slots (_battery _height _temperature ))

(defmethod ros_wrapper::State
  (:init
   (&key
    ((:battery __battery) 0)
    ((:height __height) 0.0)
    ((:temperature __temperature) 0.0)
    )
   (send-super :init)
   (setq _battery (round __battery))
   (setq _height (float __height))
   (setq _temperature (float __temperature))
   self)
  (:battery
   (&optional __battery)
   (if __battery (setq _battery __battery)) _battery)
  (:height
   (&optional __height)
   (if __height (setq _height __height)) _height)
  (:temperature
   (&optional __temperature)
   (if __temperature (setq _temperature __temperature)) _temperature)
  (:serialization-length
   ()
   (+
    ;; int64 _battery
    8
    ;; float32 _height
    4
    ;; float32 _temperature
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _battery
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _battery (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _battery) (= (length (_battery . bv)) 2)) ;; bignum
              (write-long (ash (elt (_battery . bv) 0) 0) s)
              (write-long (ash (elt (_battery . bv) 1) -1) s))
             ((and (class _battery) (= (length (_battery . bv)) 1)) ;; big1
              (write-long (elt (_battery . bv) 0) s)
              (write-long (if (>= _battery 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _battery s)(write-long (if (>= _battery 0) 0 #xffffffff) s)))
     ;; float32 _height
       (sys::poke _height (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _temperature
       (sys::poke _temperature (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _battery
#+(or :alpha :irix6 :x86_64)
      (setf _battery (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _battery (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float32 _height
     (setq _height (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _temperature
     (setq _temperature (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get ros_wrapper::State :md5sum-) "b00fd2063ed0650cb18a14280f6436f2")
(setf (get ros_wrapper::State :datatype-) "ros_wrapper/State")
(setf (get ros_wrapper::State :definition-)
      "int64 battery
float32 height
float32 temperature
")



(provide :ros_wrapper/State "b00fd2063ed0650cb18a14280f6436f2")


