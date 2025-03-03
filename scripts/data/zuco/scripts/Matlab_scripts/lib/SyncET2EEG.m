function [eeg, seq_bad, origNrChannels] = SyncET2EEG(eeg, etFile, currentPath,trigger,plot)
origNrChannels = eeg.nbchan;
if plot
eeg = pop_importeyetracker(eeg,etFile, [trigger(1,1),trigger(1,2)] ,[1,2,3,4] ,{'TIME','L_GAZE_X','L_GAZE_Y','L_AREA'},0,1,0,1); % Syncronize EEG & ET Based on Triggers
%Last digit on line above this defines if there is graphical output
else
  eeg = pop_importeyetracker(eeg,etFile, [trigger(1,1),trigger(1,2)] ,[1,2,3,4] ,{'TIME','L_GAZE_X','L_GAZE_Y','L_AREA'},0,1,0,0); % Syncronize EEG & ET Based on Triggers
end  
%saveas(gcf,[currentPath '_WISC_EYE_EEG_synchronization'],'jpg') % Save the Image to check sync-quality later
%close gcf
%timeChan = find(strcmp({eeg.chanlocs.labels}','TIME'));
%areaChan = find(strcmp({eeg.chanlocs.labels}','L_AREA'));
xgazeChan = find(strcmp({eeg.chanlocs.labels}','L_GAZE_X'));
ygazeChan = find(strcmp({eeg.chanlocs.labels}','L_GAZE_Y'));
[eeg,~,seq_bad] = RejectEyecontin(eeg,[xgazeChan:ygazeChan] ,[1 1] ,[800 600] ,5); % Reject bad Eyetracking Data TODO FUNCTION MODIFIED
%eeg = pop_detecteyemovements(eeg,[117 118] ,[119 120],7,2,0.036545,1,0,25,1,1,1,1) Saccade Detection 
new_event = [];
eeg.event(1).duration=[];
for ii = 1:size(seq_bad,1)
    new_event(1,ii).type = 'bad eye';
    % new_event(1,ii).value = 'bad eye';
    new_event(1,ii).latency = seq_bad(ii,1);
    new_event(1,ii).duration = seq_bad(ii,3);
    new_event(1,ii).urevent = size(eeg.event,2)+ii;
end

eeg.event = [eeg.event, new_event]; 
i = 1;
for ii = size(eeg.event,2)-size(new_event,2)+1:size(eeg.event,2)
    eeg.event(1,ii).duration = seq_bad(i,3);
    i = i+1;
end
for i = 1:size(eeg.event,2)
    ind_sort(i,1) = eeg.event(1,i).latency;
end
[i,or] = sort(ind_sort);
for i = 1:size(eeg.event,2)
    new_order(i,1) = eeg.event(1,or(i,1));
end
eeg.event = new_order';
end