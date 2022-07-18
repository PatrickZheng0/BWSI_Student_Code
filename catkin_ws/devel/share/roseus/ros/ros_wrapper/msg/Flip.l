;; Auto-generated. Do not edit!


(when (boundp 'ros_wrapper::Flip)
  (if (not (find-package "ROS_WRAPPER"))
    (make-package "ROS_WRAPPER"))
  (shadow 'Flip (find-package "ROS_WRAPPER")))
(unless (find-package "ROS_WRAPPER::FLIP")
  (make-package "ROS_WRAPPER::FLIP"))

(in-package "ROS")
;;//! \htmlinclude Flip.msg.html


(defclass ros_wrapper::Flip
  :super ros::object
  :slots (_direction ))

(defmethod ros_wrapper::Flip
  (:init
   (&key
    ((:direction __direction) "")
    )
   (send-super :init)
   (setq _direction (string __direction))
   self)
  (:direction
   (&optional __direction)
   (if __direction (setq _direction __direction)) _direction)
  (:serialization-length
   ()
   (+
    ;; string _direction
    4 (length _direction)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _direction
       (write-long (length _direction) s) (princ _direction s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _direction
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _direction (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get ros_wrapper::Flip :md5sum-) "326e9417def5db9a05a2704a4d8de15e")
(setf (get ros_wrapper::Flip :datatype-) "ros_wrapper/Flip")
(setf (get ros_wrapper::Flip :definition-)
      "string direction
")



(provide :ros_wrapper/Flip "326e9417def5db9a05a2704a4d8de15e")


