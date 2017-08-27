(setq make-backup-files nil)
(setq auto-save-default nil)

;(global-linum-mode t)
(tool-bar-mode -1)
(set-scroll-bar-mode 'nil)
(show-paren-mode t)
(electric-pair-mode t)

(defun c++-mode-init ()
  (setq
   c-basic-offset 4
   indent-tabs-mode nil
   tab-width 4)
  )
(add-hook 'c++-mode-hook 'c++-mode-init)

(defun insertbrac ()
  (interactive)
  (newline-and-indent)
  (when (looking-at "}")
    (newline-and-indent)
    (forward-line -1)
    (c-indent-line)))
(global-set-key (kbd "RET") 'insertbrac)
             
