
for i=20:26

x = load([num2str(i) '_quality_2981.csv']);
time = x(ceil(length(x(:,1))/2):end,2);
sample = x(ceil(length(x(:,1))/2):end,1);

dt = datetime(time/1000, 'ConvertFrom', 'posixtime','TimeZone','America/Chicago' );
createfigure(dt,sample);
% Create figure
figure1 = figure;

% Create axes
axes1 = axes('Parent',figure1);
hold(axes1,'on');
ylim([2,22])


% Create datetime plot
plot(X(find(Y==4)),Y(find(Y==4)),'Marker','o','LineStyle','none')
plot(X(find(Y==6)),Y(find(Y==6)),'Marker','*','LineStyle','none')
plot(X(find(Y==8)),Y(find(Y==8)),'Marker','h','LineStyle','none')
plot(X(find(Y==9)),Y(find(Y==9)),'Marker','^','LineStyle','none')
plot(X(find(Y==10)),Y(find(Y==10)),'Marker','+','LineStyle','none')
plot(X(find(Y==12)),Y(find(Y==12)),'Marker','.','LineStyle','none')
plot(X(find(Y==14)),Y(find(Y==14)),'Marker','d','LineStyle','none')
plot(X(find(Y==16)),Y(find(Y==16)),'Marker','s','LineStyle','none')
plot(X(find(Y==18)),Y(find(Y==18)),'Marker','v','LineStyle','none')
plot(X(find(Y==20)),Y(find(Y==20)),'Marker','p','LineStyle','none')

% Uncomment the following line to preserve the Y-limits of the axes
% ylim(axes1,[2 22]);
box(axes1,'on');
% Set the remaining axes properties
set(axes1,'YTick',[4 6 8 9 10 12 14 16 18 20],'YTickLabel',...
    {'SENSOR UNAVAILABLE','DATA LOST','SENSOR OFF BODY','SENSOR ON BODY','IMPROPER ATTACHMENT','DELAY IN ATTACHMENT','SENSOR BATTERY DOWN','PHONE BATTERY DOWN','SENSOR POWERED OFF','PHONE POWERED OFF'});
end