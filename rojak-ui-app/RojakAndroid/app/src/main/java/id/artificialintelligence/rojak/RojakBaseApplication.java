package id.artificialintelligence.rojak;

import android.app.Application;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.support.annotation.VisibleForTesting;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;

import javax.inject.Inject;

import id.artificialintelligence.rojak.di.component.ApplicationComponent;
import id.artificialintelligence.rojak.di.component.DaggerApplicationComponent;
import id.artificialintelligence.rojak.di.module.ApplicationModule;
import id.artificialintelligence.rojak.events.AuthenticationErrorEvent;
import rx.Scheduler;
import rx.schedulers.Schedulers;
import timber.log.Timber;

public class RojakBaseApplication extends Application {
    @Inject
    EventBus mEventBus;
    private Scheduler mScheduler;
    private ApplicationComponent mApplicationComponent;

    public static RojakBaseApplication get(Context context) {
        return (RojakBaseApplication) context.getApplicationContext();
    }

    @Override
    public void onCreate() {
        super.onCreate();

        boolean isDebuggable = (0 != (getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE));

        if (isDebuggable) {
            Timber.plant(new Timber.DebugTree());
        }

        mApplicationComponent = DaggerApplicationComponent.builder().applicationModule(new ApplicationModule(this)).build();

        mApplicationComponent.inject(this);
        mEventBus.register(this);
    }

    public ApplicationComponent getApplicationComponent() {
        return mApplicationComponent;
    }

    @VisibleForTesting
    public void setApplicationComponent(ApplicationComponent applicationComponent) {
        this.mApplicationComponent = applicationComponent;
    }

    public Scheduler getSubscribeScheduler() {
        if (mScheduler == null) {
            mScheduler = Schedulers.io();
        }
        return mScheduler;
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        Timber.e("########## onLowMemory ##########");
    }

    @Override
    public void onTerminate() {
        mEventBus.unregister(this);
        super.onTerminate();
    }

    @Subscribe
    public void onEvent(AuthenticationErrorEvent event) {
        Timber.e("Unauthorized! Redirect to Signin Activity..!.");
    }

}
